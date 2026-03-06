#!/usr/bin/env python3
"""
Bidirectional TOON ↔ JSON/JSONL converter
Combines json_to_toon and toon_to_json functionality
Automatically detects conversion direction based on file extension
"""
import json
import sys
import os
import re
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, NamedTuple, Optional, Tuple


# =============================================================================
# Type Definitions
# =============================================================================


class ArrayInfo(NamedTuple):
    """Information about array header in TOON format."""

    length: int
    delimiter: str
    fields: Optional[list[str]]


# =============================================================================
# Common Data Classes
# =============================================================================


class Delimiter(Enum):
    COMMA = ","
    TAB = "\t"
    PIPE = "|"


@dataclass
class EncodeOptions:
    indent_size: int = 2
    delimiter: Delimiter = Delimiter.COMMA
    length_marker: bool = False
    key_folding: bool = False
    flatten_depth: int = field(default_factory=lambda: float("inf"))


@dataclass
class DecodeOptions:
    pretty: bool = True
    indent: int = 2
    expand_paths: bool = False  # §13.4: expandPaths is OFF by default


# =============================================================================
# JSON TO TOON - Encoding Classes
# =============================================================================


class QuotingRules:
    """Determines when strings need quotes per TOON spec §7."""

    IDENTIFIER_PATTERN = re.compile(r"^[\w][\w.]*$", re.UNICODE)
    NUMBER_PATTERN = re.compile(r"^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$")
    LEADING_ZERO_PATTERN = re.compile(r"^-?0\d+")
    ARRAY_HEADER_PATTERN = re.compile(r"^\[.*\]")
    FIELD_HEADER_PATTERN = re.compile(r"^\{.*\}")

    RESERVED_LITERALS = frozenset({"true", "false", "null"})

    @classmethod
    def needs_quotes(
        cls, s: str, active_delimiter: Delimiter = Delimiter.COMMA
    ) -> bool:
        if not s:
            return True
        if s != s.strip():
            return True
        if s in cls.RESERVED_LITERALS:
            return True
        if cls._looks_like_number(s):
            return True
        if cls._contains_special_chars(s, active_delimiter):
            return True
        if s.startswith("-"):
            return True
        if cls.ARRAY_HEADER_PATTERN.match(s) or cls.FIELD_HEADER_PATTERN.match(s):
            return True
        return False

    @classmethod
    def needs_key_quotes(cls, key: str) -> bool:
        return not key or not cls.IDENTIFIER_PATTERN.match(key)

    @classmethod
    def _looks_like_number(cls, s: str) -> bool:
        return bool(cls.NUMBER_PATTERN.match(s) or cls.LEADING_ZERO_PATTERN.match(s))

    @classmethod
    def _contains_special_chars(cls, s: str, delimiter: Delimiter) -> bool:
        special = {
            delimiter.value,
            ":",
            '"',
            "\\",
            "\n",
            "\r",
            "\t",
            "[",
            "]",
            "{",
            "}",
        }
        return any(c in special for c in s)


class Escaper:
    """Handles string escaping per TOON spec."""

    ESCAPE_MAP = {"\\": "\\\\", '"': '\\"', "\n": "\\n", "\r": "\\r", "\t": "\\t"}

    @classmethod
    def escape(cls, s: str) -> str:
        return "".join(cls.ESCAPE_MAP.get(c, c) for c in s)


class TypeNormalizer:
    """Normalizes Python types to JSON-compatible values per TOON spec."""

    @classmethod
    def normalize(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, float):
            return cls._normalize_float(value)
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            return value
        if isinstance(value, (list, tuple)):
            return [cls.normalize(item) for item in value]
        if isinstance(value, dict):
            return {str(k): cls.normalize(v) for k, v in value.items()}
        return str(value)

    @classmethod
    def _normalize_float(cls, value: float) -> Any:
        if math.isnan(value) or math.isinf(value):
            return None
        return 0 if value == -0.0 else value


class NumberFormatter:
    """Formats numbers in canonical decimal form (no scientific notation)."""

    @classmethod
    def format(cls, value: float | int) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, int):
            return str(value)
        return cls._format_float(value)

    @classmethod
    def _format_float(cls, value: float) -> str:
        if value == int(value):
            return str(int(value))
        formatted = f"{value:.15g}"
        if "e" in formatted.lower():
            formatted = f"{value:.15f}".rstrip("0").rstrip(".")
        return formatted


class PrimitiveFormatter:
    """Formats primitive values to TOON string representation."""

    @classmethod
    def format(cls, value: Any, delimiter: Delimiter = Delimiter.COMMA) -> str:
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return NumberFormatter.format(value)
        s = value if isinstance(value, str) else str(value)
        if QuotingRules.needs_quotes(s, delimiter):
            return f'"{Escaper.escape(s)}"'
        return s


class ArrayClassifier:
    """Classifies arrays to determine optimal TOON format."""

    @classmethod
    def is_primitive_array(cls, arr: list) -> bool:
        return all(not isinstance(x, (dict, list)) for x in arr)

    @classmethod
    def is_tabular_eligible(cls, arr: list) -> bool:
        """
        True if arr is non-empty, all elements are dicts with the same keys
        and only primitive values.
        """
        if not arr:
            return False
        if not all(isinstance(x, dict) for x in arr):
            return False
        first_keys = set(arr[0].keys())
        for obj in arr:
            if set(obj.keys()) != first_keys:
                return False
            if any(isinstance(v, (dict, list)) for v in obj.values()):
                return False
        return True

    @classmethod
    def get_tabular_fields(cls, arr: list) -> list[str]:
        return list(arr[0].keys()) if arr else []


class IndentManager:
    """Manages indentation levels."""

    def __init__(self, size: int = 2):
        self._unit = " " * size

    def at(self, level: int) -> str:
        return self._unit * level


class HeaderBuilder:
    """Builds array headers per TOON spec."""

    def __init__(self, options: EncodeOptions):
        self.options = options

    def build_primitive_header(self, key: str | None, length: int) -> str:
        return self._build_simple_header(key, length)

    def build_list_header(self, key: str | None, length: int) -> str:
        return self._build_simple_header(key, length)

    def build_tabular_header(
        self, key: str | None, length: int, fields: list[str]
    ) -> str:
        length_str = self._format_length(length)
        delimiter_marker = self._get_delimiter_marker()
        # Per §9/§11: field names in {f1,f2} are ALWAYS comma-separated
        fields_str = ",".join(fields)
        prefix = "" if key is None else self._format_key(key)
        return f"{prefix}[{length_str}{delimiter_marker}]{{{fields_str}}}:"

    def _build_simple_header(self, key: str | None, length: int) -> str:
        length_str = self._format_length(length)
        prefix = "" if key is None else self._format_key(key)
        return f"{prefix}[{length_str}]:"

    def _format_length(self, length: int) -> str:
        return f"#{length}" if self.options.length_marker else str(length)

    def _format_key(self, key: str) -> str:
        if QuotingRules.needs_key_quotes(key):
            return f'"{Escaper.escape(key)}"'
        return key

    def _get_delimiter_marker(self) -> str:
        if self.options.delimiter == Delimiter.TAB:
            return " "
        if self.options.delimiter == Delimiter.PIPE:
            return "|"
        return ""


class KeyFolder:
    """Implements key folding for nested single-key objects."""

    SAFE_SEGMENT_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    @classmethod
    def can_fold(cls, key: str, value: Any, depth: int, max_depth: float) -> bool:
        return (
            depth < max_depth
            and cls.SAFE_SEGMENT_PATTERN.match(key) is not None
            and isinstance(value, dict)
            and len(value) == 1
        )

    @classmethod
    def fold_path(cls, obj: dict, max_depth: float) -> tuple[str, Any]:
        """Returns (folded_key, leaf_value) for foldable chains."""
        segments: list[str] = []
        current = obj
        depth = 0
        while isinstance(current, dict) and len(current) == 1 and depth < max_depth:
            key = next(iter(current.keys()))
            if not cls.SAFE_SEGMENT_PATTERN.match(key):
                break
            segments.append(key)
            current = current[key]
            depth += 1
        return ".".join(segments), current


# =============================================================================
# Render Context — Template Method for array encoding
# =============================================================================


@dataclass
class RenderContext:
    """
    Describes how an array block should be rendered within TOONEncoder.

    TOONEncoder needs to produce array lines in three structurally identical
    but superficially different contexts:

      A) TOP-LEVEL / NESTED OBJECT context
         - header is indented with indent.at(level)
         - rows are indented with indent.at(level + 1)
         - result is returned as a joined str

      B) ADDITIONAL DICT ENTRY inside a list item
         - identical to A, but result is returned as list[str]
           (the caller stitches it into a larger list)

      C) FIRST ENTRY of a list item (after the "- " dash)
         - header has NO indent (the "- " prefix is added by the caller)
         - rows use indent.at(level + row_indent_offset)  [= level+3 for first-entry]
         - result is returned as joined str

    Without this context object the encoder needs six separate methods
    (_encode_tabular_array, _encode_tabular_entry, _format_first_tabular_entry
    and their list-array twins) whose bodies are >80% identical.
    """

    header_indent: str  # prefix for the header line
    row_indent_offset: int  # extra levels added to `level` for row indentation
    returns_list: bool  # True → return list[str]; False → return joined str

    # Named constructors for the three contexts:

    @classmethod
    def top_level(cls, indent: IndentManager, level: int) -> "RenderContext":
        return cls(
            header_indent=indent.at(level),
            row_indent_offset=1,
            returns_list=False,
        )

    @classmethod
    def dict_entry(cls, indent: IndentManager, level: int) -> "RenderContext":
        return cls(
            header_indent=indent.at(level),
            row_indent_offset=1,
            returns_list=True,
        )

    @classmethod
    def first_list_entry(cls) -> "RenderContext":
        """Header has no indent (caller owns the '- ' prefix)."""
        return cls(
            header_indent="",
            row_indent_offset=3,  # TOON spec quirk for first-entry arrays
            returns_list=False,
        )


class TOONEncoder:
    """Main encoder class — converts Python data to TOON format."""

    def __init__(self, options: EncodeOptions | None = None):
        self.options = options or EncodeOptions()
        self.indent = IndentManager(self.options.indent_size)
        self.header = HeaderBuilder(self.options)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def encode(self, data: Any) -> str:
        normalized = TypeNormalizer.normalize(data)
        return self._encode_value(normalized, level=0, key=None)

    # -------------------------------------------------------------------------
    # Value dispatch
    # -------------------------------------------------------------------------

    def _encode_value(self, value: Any, level: int, key: str | None) -> str:
        if isinstance(value, dict):
            return self._encode_object(value, level, key)
        if isinstance(value, list):
            return self._encode_array(value, level, key)
        return self._encode_primitive(value, level, key)

    # -------------------------------------------------------------------------
    # Object encoding
    # -------------------------------------------------------------------------

    def _encode_object(self, obj: dict, level: int, key: str | None) -> str:
        if not obj:
            return f"{self.indent.at(level)}{self._format_key(key)}:" if key else ""

        lines: list[str] = []
        if key is not None:
            lines.append(f"{self.indent.at(level)}{self._format_key(key)}:")
            level += 1

        # FIX P2: renamed loop variable to avoid shadowing the `key` parameter
        for item_key, value in obj.items():
            if self.options.key_folding and KeyFolder.can_fold(
                item_key, value, 0, self.options.flatten_depth
            ):
                folded_key, leaf = KeyFolder.fold_path(
                    {item_key: value}, self.options.flatten_depth
                )
                lines.append(self._encode_value(leaf, level, folded_key))
            else:
                lines.append(self._encode_value(value, level, item_key))

        return "\n".join(lines)

    # -------------------------------------------------------------------------
    # Array encoding (top-level / nested-in-object)
    # -------------------------------------------------------------------------

    def _encode_array(self, arr: list, level: int, key: str | None) -> str:
        ctx = RenderContext.top_level(self.indent, level)
        lines = self._render_array_lines(arr, key, level, ctx)
        if isinstance(lines, list):
            return "\n".join(lines)
        return lines  # str

    # -------------------------------------------------------------------------
    # Core Template Method — renders any array in any context
    # -------------------------------------------------------------------------

    def _render_array_lines(
        self,
        arr: list,
        key: str | None,
        level: int,
        ctx: RenderContext,
    ) -> str | list[str]:
        """
        Unified array renderer (Template Method).

        Builds the header line and body lines for primitive, tabular, and list
        arrays. The three callers supply a RenderContext that controls:
          - how the header is indented
          - the row indent offset
          - whether to return str or list[str]

        This single method replaces six near-identical methods that existed
        in the original implementation.
        """
        if not arr:
            header = self.header.build_list_header(key, 0)
            result = [f"{ctx.header_indent}{header}"]
            return result if ctx.returns_list else "\n".join(result)

        if ArrayClassifier.is_primitive_array(arr):
            return self._render_primitive_array(arr, key, level, ctx)

        if ArrayClassifier.is_tabular_eligible(arr):
            return self._render_tabular_array(arr, key, level, ctx)

        return self._render_list_array(arr, key, level, ctx)

    def _render_primitive_array(
        self, arr: list, key: str | None, level: int, ctx: RenderContext
    ) -> str | list[str]:
        delimiter = self.options.delimiter.value
        items_str = delimiter.join(
            PrimitiveFormatter.format(x, self.options.delimiter) for x in arr
        )
        header = self.header.build_primitive_header(key, len(arr))
        result = [f"{ctx.header_indent}{header} {items_str}"]
        return result if ctx.returns_list else "\n".join(result)

    def _render_tabular_array(
        self, arr: list, key: str | None, level: int, ctx: RenderContext
    ) -> str | list[str]:
        fields = ArrayClassifier.get_tabular_fields(arr)
        header = self.header.build_tabular_header(key, len(arr), fields)
        row_indent = self.indent.at(level + ctx.row_indent_offset)
        delimiter = self.options.delimiter.value

        lines: list[str] = [f"{ctx.header_indent}{header}"]
        for obj in arr:
            row = delimiter.join(
                PrimitiveFormatter.format(obj[f], self.options.delimiter)
                for f in fields
            )
            lines.append(f"{row_indent}{row}")

        return lines if ctx.returns_list else "\n".join(lines)

    def _render_list_array(
        self, arr: list, key: str | None, level: int, ctx: RenderContext
    ) -> str | list[str]:
        header = self.header.build_list_header(key, len(arr))
        lines: list[str] = [f"{ctx.header_indent}{header}"]
        for item in arr:
            lines.extend(self._encode_list_item(item, level + 1))
        return lines if ctx.returns_list else "\n".join(lines)

    # -------------------------------------------------------------------------
    # List item encoding
    # -------------------------------------------------------------------------

    def _encode_list_item(self, item: Any, level: int) -> list[str]:
        indent = self.indent.at(level)
        if isinstance(item, dict):
            return self._encode_dict_list_item(item, level)
        if isinstance(item, list):
            return self._encode_array_list_item(item, level)
        formatted = PrimitiveFormatter.format(item, self.options.delimiter)
        return [f"{indent}- {formatted}"]

    def _encode_dict_list_item(self, obj: dict, level: int) -> list[str]:
        indent = self.indent.at(level)
        if not obj:
            return [f"{indent}-"]

        entries = list(obj.items())
        first_key, first_value = entries[0]
        lines: list[str] = [
            f"{indent}- {self._format_first_entry(first_key, first_value, level)}"
        ]

        for item_key, value in entries[1:]:
            lines.extend(self._encode_dict_entry(item_key, value, level + 1))

        return lines

    def _format_first_entry(self, key: str, value: Any, level: int) -> str:
        """
        Format the first key-value of a dict list item (shares the dash line).
        Arrays in this position use RenderContext.first_list_entry().
        """
        if isinstance(value, dict):
            nested = self._encode_object(value, level + 2, None)
            return (
                f"{self._format_key(key)}:\n{nested}"
                if nested
                else f"{self._format_key(key)}:"
            )

        if isinstance(value, list):
            ctx = RenderContext.first_list_entry()
            result = self._render_array_lines(value, key, level, ctx)
            return result if isinstance(result, str) else "\n".join(result)

        formatted = PrimitiveFormatter.format(value, self.options.delimiter)
        return f"{self._format_key(key)}: {formatted}"

    def _encode_dict_entry(self, key: str, value: Any, level: int) -> list[str]:
        indent = self.indent.at(level)
        if isinstance(value, dict):
            if not value:
                return [f"{indent}{self._format_key(key)}:"]
            nested = self._encode_object(value, level + 1, None)
            return (
                [f"{indent}{self._format_key(key)}:", nested]
                if nested
                else [f"{indent}{self._format_key(key)}:"]
            )

        if isinstance(value, list):
            ctx = RenderContext.dict_entry(self.indent, level)
            result = self._render_array_lines(value, key, level, ctx)
            lines = result if isinstance(result, list) else [result]
            return [
                f"{indent}{line}" if not line.startswith(indent) else line
                for line in lines
            ]

        formatted = PrimitiveFormatter.format(value, self.options.delimiter)
        return [f"{indent}{self._format_key(key)}: {formatted}"]

    def _encode_array_list_item(self, arr: list, level: int) -> list[str]:
        indent = self.indent.at(level)
        if not arr:
            return [f"{indent}- [0]:"]
        if ArrayClassifier.is_primitive_array(arr):
            delimiter = self.options.delimiter.value
            items_str = delimiter.join(
                PrimitiveFormatter.format(x, self.options.delimiter) for x in arr
            )
            return [f"{indent}- [{len(arr)}]: {items_str}"]

        lines = [f"{indent}- [{len(arr)}]:"]
        for item in arr:
            lines.extend(self._encode_list_item(item, level + 1))
        return lines

    # -------------------------------------------------------------------------
    # Primitive encoding
    # -------------------------------------------------------------------------

    def _encode_primitive(self, value: Any, level: int, key: str | None) -> str:
        formatted = PrimitiveFormatter.format(value, self.options.delimiter)
        if key is None:
            return formatted
        return f"{self.indent.at(level)}{self._format_key(key)}: {formatted}"

    def _format_key(self, key: str) -> str:
        if QuotingRules.needs_key_quotes(key):
            return f'"{Escaper.escape(key)}"'
        return key


# =============================================================================
# TOON TO JSON — Decoding Classes
# =============================================================================


@dataclass
class _ParseState:
    """
    Encapsulates mutable parsing state.

    Isolating this into a separate object makes TOONParser stateless
    (and thus safe to reuse across threads) while keeping the state
    co-located for readability.
    """

    lines: list[str]
    current_line: int = 0

    def peek(self, offset: int = 0) -> Optional[str]:
        idx = self.current_line + offset
        return self.lines[idx] if idx < len(self.lines) else None

    def consume(self) -> Optional[str]:
        if self.current_line >= len(self.lines):
            return None
        line = self.lines[self.current_line]
        self.current_line += 1
        return line

    @staticmethod
    def indent_of(line: str) -> int:
        return len(line) - len(line.lstrip())


class TOONParser:
    """Stateless parser for TOON format files."""

    INDENT_STEP = 2

    def __init__(self, expand_paths: bool = False):
        self.expand_paths = expand_paths  # §13.4: OFF by default

    def parse(self, content: str) -> Any:
        """Parse TOON content and return a Python object."""
        state = _ParseState(lines=content.split("\n"))
        return self._parse_value(state, 0)

    # -------------------------------------------------------------------------
    # Core parsing
    # -------------------------------------------------------------------------

    def _parse_value(self, st: _ParseState, expected_indent: int) -> Any:
        line = st.peek()
        if line is None:
            return None

        actual_indent = st.indent_of(line)
        if actual_indent < expected_indent:
            return None

        stripped = line.strip()
        if not stripped:
            st.consume()
            return self._parse_value(st, expected_indent)

        if stripped.startswith("-"):
            return None

        if ":" in stripped:
            return self._parse_object(st, expected_indent)

        st.consume()
        return self._parse_primitive(stripped)

    def _parse_object(self, st: _ParseState, expected_indent: int) -> dict:
        obj: dict = {}

        while st.current_line < len(st.lines):
            line = st.peek()
            if line is None:
                break
            actual_indent = st.indent_of(line)
            if actual_indent < expected_indent:
                break
            if actual_indent > expected_indent:
                st.consume()
                continue

            stripped = line.strip()
            if not stripped or ":" not in stripped:
                break

            key, value = self._parse_key_value_line(st, stripped, expected_indent)
            if key is None:
                break

            if "." in key and "[" not in key and self.expand_paths:
                self._set_nested_key(obj, key, value)
            else:
                obj[key] = value

        return obj

    def _parse_key_value_line(
        self, st: _ParseState, line: str, current_indent: int
    ) -> Tuple[Optional[str], Any]:
        st.consume()
        colon_pos = self._find_key_separator(line)
        if colon_pos == -1:
            return None, None

        key_part = line[:colon_pos].strip()
        value_part = line[colon_pos + 1 :].strip()
        key, array_info = self._parse_key_with_array_header(key_part)

        if array_info:
            length, delimiter, fields = array_info
            if fields:
                return key, self._parse_tabular_array(
                    st, current_indent, length, fields, delimiter
                )
            if value_part:
                return key, self._parse_inline_array(value_part, delimiter)
            return key, self._parse_list_array(st, current_indent, length)

        if value_part:
            return key, self._parse_primitive(value_part)

        value = self._parse_value(st, current_indent + self.INDENT_STEP)
        return key, value if value is not None else {}

    # -------------------------------------------------------------------------
    # Header / key parsing
    # -------------------------------------------------------------------------

    def _find_key_separator(self, line: str) -> int:
        """
        Return index of the key-separating colon, ignoring colons inside
        quoted strings, brackets, or braces. Returns -1 if not found.
        """
        bracket_depth = brace_depth = 0
        in_quotes = False
        for i, char in enumerate(line):
            if char == '"' and (i == 0 or line[i - 1] != "\\"):
                in_quotes = not in_quotes
            elif not in_quotes:
                if char == "[":
                    bracket_depth += 1
                elif char == "]":
                    bracket_depth -= 1
                elif char == "{":
                    brace_depth += 1
                elif char == "}":
                    brace_depth -= 1
                elif char == ":" and bracket_depth == 0 and brace_depth == 0:
                    return i
        return -1

    def _parse_key_with_array_header(
        self, key_part: str
    ) -> Tuple[str, Optional[ArrayInfo]]:
        match = re.search(r"\[(\#?\d+)(\s|\|)?\](?:\{([^}]+)\})?$", key_part)
        if not match:
            return self._unquote_string(key_part), None

        length_str, delimiter_marker, fields_str = match.groups()
        length = int(length_str.lstrip("#"))
        delimiter = self._delimiter_from_marker(delimiter_marker)

        fields = None
        if fields_str:
            # Per §9/§11: field names in {f1,f2} are ALWAYS comma-separated
            fields = [f.strip() for f in self._split_by_delimiter(fields_str, ",")]

        key = self._unquote_string(key_part[: match.start()].strip()) or None
        return key, ArrayInfo(length, delimiter, fields)

    # -------------------------------------------------------------------------
    # Array parsing
    # -------------------------------------------------------------------------

    def _parse_tabular_array(
        self,
        st: _ParseState,
        current_indent: int,
        length: int,
        fields: list,
        delimiter: str,
    ) -> list:
        result = []
        for _ in range(length):
            line = st.peek()
            if line is None or st.indent_of(line) < current_indent:
                break
            st.consume()
            values = self._split_by_delimiter(line.strip(), delimiter)
            row = {
                field: (
                    self._parse_primitive(values[i].strip())
                    if i < len(values)
                    else None
                )
                for i, field in enumerate(fields)
            }
            result.append(row)
        return result

    def _parse_inline_array(self, value_part: str, delimiter: str) -> list:
        return [
            self._parse_primitive(v.strip())
            for v in self._split_by_delimiter(value_part, delimiter)
        ]

    def _parse_list_array(
        self, st: _ParseState, current_indent: int, length: int
    ) -> list:
        result = []
        for _ in range(length):
            line = st.peek()
            if line is None or st.indent_of(line) < current_indent:
                break
            stripped = line.strip()
            if not stripped.startswith("-"):
                break
            st.consume()
            content = stripped[1:].strip()
            if not content:
                item = self._parse_value(st, st.indent_of(line) + self.INDENT_STEP)
                result.append(item if item is not None else {})
            else:
                result.append(
                    self._parse_inline_list_item(st, content, st.indent_of(line))
                )
        return result

    def _parse_inline_list_item(
        self, st: _ParseState, content: str, item_indent: int
    ) -> Any:
        array_result = self._try_parse_as_array(st, content, item_indent)
        if array_result is not None:
            return array_result

        obj_result = self._try_parse_as_object(st, content, item_indent)
        if obj_result is not None:
            return obj_result

        return self._parse_primitive(content)

    def _try_parse_as_array(
        self, st: _ParseState, content: str, item_indent: int
    ) -> Any | None:
        m = re.match(r"\[(\#?\d+)(\s|\|)?\](?:\{([^}]+)\})?:\s*(.*)", content)
        if not m:
            return None
        length_str, delimiter_marker, fields_str, rest = m.groups()
        length = int(length_str.lstrip("#"))
        delimiter = self._delimiter_from_marker(delimiter_marker)

        if fields_str:
            fields = [
                f.strip() for f in self._split_by_delimiter(fields_str, delimiter)
            ]
            return self._parse_tabular_array(st, item_indent, length, fields, delimiter)
        if rest:
            return self._parse_inline_array(rest, delimiter)
        return self._parse_list_array(st, item_indent, length)

    def _try_parse_as_object(
        self, st: _ParseState, content: str, item_indent: int
    ) -> dict | None:
        if ":" not in content:
            return None
        colon_pos = self._find_key_separator(content)
        if colon_pos == -1:
            return None

        key_part = content[:colon_pos].strip()
        value_part = content[colon_pos + 1 :].strip()
        key, array_info = self._parse_key_with_array_header(key_part)

        obj = {key: self._parse_object_value(st, array_info, value_part, item_indent)}
        self._parse_additional_object_keys(st, obj, item_indent)
        return obj

    def _parse_object_value(
        self,
        st: _ParseState,
        array_info: Optional[ArrayInfo],
        value_part: str,
        item_indent: int,
    ) -> Any:
        if not array_info:
            return (
                self._parse_primitive(value_part)
                if value_part
                else self._parse_value(st, item_indent + self.INDENT_STEP)
            )
        length, delimiter, fields = array_info
        if fields:
            return self._parse_tabular_array(st, item_indent, length, fields, delimiter)
        if value_part:
            return self._parse_inline_array(value_part, delimiter)
        return self._parse_list_array(st, item_indent, length)

    def _parse_additional_object_keys(
        self, st: _ParseState, obj: dict, item_indent: int
    ) -> None:
        while True:
            next_line = st.peek()
            if next_line is None:
                break
            if st.indent_of(next_line) <= item_indent:
                break
            next_stripped = next_line.strip()
            if not next_stripped or ":" not in next_stripped:
                break
            next_key, next_value = self._parse_key_value_line(
                st, next_stripped, item_indent + self.INDENT_STEP
            )
            if not next_key:
                break
            obj[next_key] = next_value

    # -------------------------------------------------------------------------
    # Primitive / string helpers
    # -------------------------------------------------------------------------

    def _parse_primitive(self, value: str) -> Any:
        value = value.strip()
        if not value or value == "null":
            return None
        if value == "true":
            return True
        if value == "false":
            return False
        if value.startswith('"') and value.endswith('"'):
            return self._unescape_string(value[1:-1])
        try:
            return (
                float(value) if ("." in value or "e" in value.lower()) else int(value)
            )
        except ValueError:
            return value

    def _unquote_string(self, s: str) -> str:
        s = s.strip()
        if s.startswith('"') and s.endswith('"'):
            return self._unescape_string(s[1:-1])
        return s

    def _unescape_string(self, s: str) -> str:
        return (
            s.replace("\\n", "\n")
            .replace("\\r", "\r")
            .replace("\\t", "\t")
            .replace('\\"', '"')
            .replace("\\\\", "\\")
        )

    def _split_by_delimiter(self, text: str, delimiter: str) -> list[str]:
        """Split text by delimiter, respecting quoted strings."""
        parts: list[str] = []
        current: list[str] = []
        in_quotes = False
        i = 0
        while i < len(text):
            char = text[i]
            if char == '"' and (i == 0 or text[i - 1] != "\\"):
                in_quotes = not in_quotes
            elif char == delimiter and not in_quotes:
                parts.append("".join(current))
                current = []
                i += 1
                continue
            current.append(char)
            i += 1
        if current:
            parts.append("".join(current))
        return parts

    @staticmethod
    def _delimiter_from_marker(marker: str | None) -> str:
        if marker == "|":
            return "|"
        if marker == " ":
            return "\t"
        return ","

    def _set_nested_key(self, obj: dict, key_path: str, value: Any) -> None:
        parts = key_path.split(".")
        current = obj
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value


# =============================================================================
# Bidirectional Converter
# =============================================================================


@dataclass
class ConversionResult:
    """Summary of a batch conversion operation."""

    converted: int = 0
    errors: int = 0

    def record_success(self) -> None:
        self.converted += 1

    def record_error(self, label: str, error: Exception) -> None:
        print(f"⚠️  {label}: {error}")
        self.errors += 1

    def report(self, output_path: str) -> None:
        print(f"✅ Converted {self.converted} items to {output_path}")
        if self.errors:
            print(f"⚠️  {self.errors} items skipped due to errors")


class BidirectionalConverter:
    """Handles bidirectional conversion between TOON and JSON formats."""

    def __init__(
        self,
        encode_options: EncodeOptions | None = None,
        decode_options: DecodeOptions | None = None,
    ):
        self.encoder = TOONEncoder(encode_options)
        self.decode_options = decode_options or DecodeOptions()
        self.parser = TOONParser(expand_paths=self.decode_options.expand_paths)

    def convert_file(self, input_path: str, output_path: str | None = None) -> None:
        """
        Convert file automatically detecting direction from extension.

        Supported conversions:
          .json  →  .toon
          .jsonl →  folder of .toon files
          .toon  →  .json
          folder of .toon  →  .jsonl
        """
        if os.path.isdir(input_path):
            output_path = (
                output_path or f"{os.path.basename(input_path.rstrip('/'))}.jsonl"
            )
            self._convert_folder_to_jsonl(input_path, output_path)
        elif input_path.endswith(".jsonl"):
            output_path = (
                output_path
                or f"{os.path.splitext(os.path.basename(input_path))[0]}_toons"
            )
            self._convert_jsonl_to_toon(input_path, output_path)
        elif input_path.endswith(".json"):
            output_path = output_path or os.path.splitext(input_path)[0] + ".toon"
            self._convert_json_to_toon(input_path, output_path)
        elif input_path.endswith(".toon"):
            output_path = output_path or os.path.splitext(input_path)[0] + ".json"
            self._convert_toon_to_json(input_path, output_path)
        else:
            raise ValueError(f"Unsupported file type: {input_path}")

    # -------------------------------------------------------------------------
    # Single-file conversions
    # -------------------------------------------------------------------------

    def _convert_json_to_toon(self, input_path: str, output_path: str) -> None:
        data = self._read_json(input_path)
        toon_content = self.encoder.encode(data)
        self._write_toon(output_path, toon_content)
        print(f"✅ {input_path} → {output_path}")

    def _convert_toon_to_json(self, input_path: str, output_path: str) -> None:
        toon_content = self._read_toon(input_path)
        data = self.parser.parse(toon_content)
        self._write_json(output_path, data)
        print(f"✅ {input_path} → {output_path}")

    # -------------------------------------------------------------------------
    # Batch conversions
    # -------------------------------------------------------------------------

    def _convert_jsonl_to_toon(self, input_path: str, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        result = ConversionResult()

        with open(input_path, "r", encoding="utf-8") as f:
            for i, raw_line in enumerate(f):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    toon_content = self.encoder.encode(data)
                    output_file = os.path.join(output_dir, f"{base_name}_{i:04d}.toon")
                    self._write_toon(output_file, toon_content)
                    result.record_success()
                except json.JSONDecodeError as e:
                    result.record_error(f"Line {i}: Invalid JSON", e)
                except OSError as e:
                    result.record_error(f"Line {i}: File write error", e)

        result.report(f"{output_dir}/")

    def _convert_folder_to_jsonl(self, input_folder: str, output_path: str) -> None:
        toon_files = sorted(f for f in os.listdir(input_folder) if f.endswith(".toon"))
        if not toon_files:
            print(f"⚠️  No .toon files found in {input_folder}")
            return

        result = ConversionResult()
        with open(output_path, "w", encoding="utf-8") as outfile:
            for toon_file in toon_files:
                toon_path = os.path.join(input_folder, toon_file)
                try:
                    data = self.parser.parse(self._read_toon(toon_path))
                    outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
                    result.record_success()
                except OSError as e:
                    result.record_error(f"{toon_file}: File read error", e)
                except (ValueError, KeyError) as e:
                    result.record_error(f"{toon_file}: Parse error", e)
                except Exception as e:  # noqa: BLE001
                    result.record_error(
                        f"{toon_file}: Unexpected error ({type(e).__name__})", e
                    )

        result.report(output_path)

    # -------------------------------------------------------------------------
    # File I/O helpers
    # -------------------------------------------------------------------------

    def _read_json(self, path: str) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _read_toon(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _write_json(self, path: str, data: Any) -> None:
        with open(path, "w", encoding="utf-8") as f:
            if self.decode_options.pretty:
                json.dump(
                    data, f, ensure_ascii=False, indent=self.decode_options.indent
                )
            else:
                json.dump(data, f, ensure_ascii=False)

    def _write_toon(self, path: str, content: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


# =============================================================================
# CLI
# =============================================================================


class CLI:
    """Command line interface handler."""

    @staticmethod
    def run(args: list[str]) -> None:
        if len(args) < 2:
            CLI._print_usage()
            sys.exit(1)

        input_path = args[1]
        if not os.path.exists(input_path):
            print(f"❌ File or folder not found: {input_path}")
            sys.exit(1)

        try:
            converter = BidirectionalConverter(
                CLI._parse_encode_options(args),
                CLI._parse_decode_options(args),
            )
            converter.convert_file(input_path, CLI._get_output_path(args))
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    @staticmethod
    def _get_output_path(args: list[str]) -> Optional[str]:
        for i, arg in enumerate(args):
            if arg in ("-o", "--output") and i + 1 < len(args):
                return args[i + 1]
        if len(args) > 2 and not args[2].startswith("-"):
            return args[2]
        return None

    @staticmethod
    def _parse_encode_options(args: list[str]) -> EncodeOptions:
        options = EncodeOptions()
        if "--tab" in args:
            options.delimiter = Delimiter.TAB
        if "--pipe" in args:
            options.delimiter = Delimiter.PIPE
        if "--length-marker" in args:
            options.length_marker = True
        if "--key-folding" in args:
            options.key_folding = True
        return options

    @staticmethod
    def _parse_decode_options(args: list[str]) -> DecodeOptions:
        options = DecodeOptions()
        if "--compact" in args:
            options.pretty = False
        if "--expand-paths" in args:
            options.expand_paths = True
        if "--indent" in args:
            idx = args.index("--indent")
            if idx + 1 < len(args):
                try:
                    options.indent = int(args[idx + 1])
                except ValueError:
                    pass
        return options

    @staticmethod
    def _print_usage() -> None:
        print(
            """\
Bidirectional TOON ↔ JSON/JSONL Converter

Usage: python toon_json_converter.py <input> [output] [options]

Automatic direction detection:
  .json file      → .toon file
  .jsonl file     → folder of .toon files
  .toon file      → .json file
  folder of .toon → .jsonl file

Options:
  -o, --output <path>   Output file/folder path

  Encoding options (JSON → TOON):
    --tab               Use tab delimiter
    --pipe              Use pipe delimiter
    --length-marker     Add # prefix to array lengths
    --key-folding       Enable key folding for nested objects

  Decoding options (TOON → JSON):
    --compact           Minified JSON output
    --indent <n>        Set indentation spaces (default: 2)
    --expand-paths      Expand dotted keys into nested objects (§13.4, off by default)
"""
        )


if __name__ == "__main__":
    CLI.run(sys.argv)
