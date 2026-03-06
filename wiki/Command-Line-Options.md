> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# Command-Line Options

> Comprehensive guide to all command-line options and flags

## Overview

The TOON JSON Converter provides separate option sets for encoding (JSON → TOON) and decoding (TOON → JSON) operations.

  **Important:** Encoding options only apply when converting TO TOON format. Decoding options only apply when converting TO JSON format.

## General Options

### Output Path

  Specify the output file or folder path.

  **Default:** Auto-generated based on input filename

  **Applies to:** All conversion modes

  **Source:** toon\_json\_converter.py:1204-1210

#### Usage

```bash  theme={null}
# Using short flag
python toon_json_converter.py input.json -o custom_output.toon

# Using long flag
python toon_json_converter.py input.toon --output result.json

# Positional argument (alternative)
python toon_json_converter.py input.json output.toon
```

#### Auto-Generated Paths

When output is omitted, the converter generates the path automatically:

| Input Pattern | Generated Output | Example                            |
| ------------- | ---------------- | ---------------------------------- |
| `*.json`      | `*.toon`         | `data.json` → `data.toon`          |
| `*.jsonl`     | `*_toons/`       | `logs.jsonl` → `logs_toons/`       |
| `*.toon`      | `*.json`         | `config.toon` → `config.json`      |
| `folder/`     | `folder.jsonl`   | `data_toons/` → `data_toons.jsonl` |

Source reference: `toon_json_converter.py:1061-1076`

## Encoding Options (JSON → TOON)

These options control how JSON data is encoded into TOON format.

### Delimiter Options

  Use tab (`\t`) as the delimiter for tabular array values.

  **Default:** Comma (`,`)

  **Applies to:** Tabular arrays (arrays of objects with uniform keys)

  **Source:** toon\_json\_converter.py:1215-1216

  **Data structure:** Sets `EncodeOptions.delimiter = Delimiter.TAB`

#### Example: Default Comma Delimiter

**Input JSON:**

```json  theme={null}
{
  "users": [
    {"name": "Alice", "age": 30, "city": "NYC"},
    {"name": "Bob", "age": 25, "city": "LA"}
  ]
}
```

**Command:**

```bash  theme={null}
python toon_json_converter.py users.json
```

**Output:**

```toon  theme={null}
users[2]{name,age,city}:
  Alice, 30, NYC
  Bob, 25, LA
```

#### Example: Tab Delimiter

**Command:**

```bash  theme={null}
python toon_json_converter.py users.json users_tab.toon --tab
```

**Output:**

```toon  theme={null}
users[2 ]{name,age,city}:
  Alice	30	NYC
  Bob	25	LA
```

  **Header marker:** When using `--tab`, the header displays a space marker (` `) to indicate tab-separated values.

  Use pipe (`|`) as the delimiter for tabular array values.

  **Default:** Comma (`,`)

  **Applies to:** Tabular arrays (arrays of objects with uniform keys)

  **Source:** toon\_json\_converter.py:1217-1218

  **Data structure:** Sets `EncodeOptions.delimiter = Delimiter.PIPE`

#### Example: Pipe Delimiter

**Command:**

```bash  theme={null}
python toon_json_converter.py users.json users_pipe.toon --pipe
```

**Output:**

```toon  theme={null}
users[2|]{name,age,city}:
  Alice|30|NYC
  Bob|25|LA
```

  **Header marker:** When using `--pipe`, the header displays a pipe marker (`|`) inside the brackets.

#### Delimiter Comparison

| Option   | Delimiter Character | Header Marker | Use Case                   |
| -------- | ------------------- | ------------- | -------------------------- |
| Default  | Comma (`,`)         | None          | Standard CSV-like data     |
| `--tab`  | Tab (`\t`)          | Space (` `)   | Tab-separated values (TSV) |
| `--pipe` | Pipe (`\|`)         | Pipe (`\|`)   | Pipe-delimited data        |

### Array Length Marker

  Add `#` prefix to array length indicators in headers.

  **Default:** No prefix

  **Applies to:** All array types (primitive, tabular, list)

  **Source:** toon\_json\_converter.py:1219-1220

  **Data structure:** Sets `EncodeOptions.length_marker = True`

#### Example: Without Length Marker (Default)

**Input JSON:**

```json  theme={null}
{
  "tags": ["python", "json", "converter"],
  "scores": [95, 87, 92]
}
```

**Command:**

```bash  theme={null}
python toon_json_converter.py data.json
```

**Output:**

```toon  theme={null}
tags[3]: python, json, converter
scores[3]: 95, 87, 92
```

#### Example: With Length Marker

**Command:**

```bash  theme={null}
python toon_json_converter.py data.json data.toon --length-marker
```

**Output:**

```toon  theme={null}
tags[#3]: python, json, converter
scores[#3]: 95, 87, 92
```

#### Benefits

* **Improved readability:** The `#` makes array lengths visually distinct from index notation
* **Parsing clarity:** Helps distinguish array headers from potential index-based keys
* **Spec compliance:** Follows TOON optional syntax for array length notation

### Key Folding

  Enable key folding for nested single-key objects. Converts chains of objects with single keys into dotted path notation.

  **Default:** Disabled

  **Applies to:** Nested objects where each level has exactly one key

  **Requirements:** Keys must match pattern `[A-Za-z_][A-Za-z0-9_]*` (alphanumeric + underscore, starting with letter/underscore)

  **Source:** toon\_json\_converter.py:1221-1222

  **Data structure:** Sets `EncodeOptions.key_folding = True`

  **Implementation:** KeyFolder class (toon\_json\_converter.py:278-306)

#### Example: Without Key Folding (Default)

**Input JSON:**

```json  theme={null}
{
  "server": {
    "config": {
      "network": {
        "port": 8080
      }
    }
  }
}
```

**Command:**

```bash  theme={null}
python toon_json_converter.py config.json
```

**Output:**

```toon  theme={null}
server:
  config:
    network:
      port: 8080
```

#### Example: With Key Folding

**Command:**

```bash  theme={null}
python toon_json_converter.py config.json config.toon --key-folding
```

**Output:**

```toon  theme={null}
server.config.network.port: 8080
```

#### Key Folding Rules

Key folding applies when **ALL** of these conditions are met:

1. ✅ Object has exactly **one key**
2. ✅ Key matches pattern `[A-Za-z_][A-Za-z0-9_]*`
3. ✅ Value is another object (continues the chain)

Key folding **stops** when:

* ❌ Object has multiple keys
* ❌ Key contains special characters (`.`, `-`, etc.)
* ❌ Value is not an object (primitive, array, etc.)
* ❌ Max depth reached (default: infinite)

#### Example: Partial Key Folding

**Input JSON:**

```json  theme={null}
{
  "database": {
    "connection": {
      "host": "localhost",
      "port": 5432
    }
  }
}
```

**Command:**

```bash  theme={null}
python toon_json_converter.py db.json db.toon --key-folding
```

**Output:**

```toon  theme={null}
database.connection:
  host: localhost
  port: 5432
```

  Folding stops at `connection` because the next level has **two keys** (`host` and `port`).

#### Example: Invalid Keys for Folding

**Input JSON:**

```json  theme={null}
{
  "app-config": {
    "api.endpoint": {
      "url": "https://api.example.com"
    }
  }
}
```

**Command:**

```bash  theme={null}
python toon_json_converter.py app.json app.toon --key-folding
```

**Output:**

```toon  theme={null}
"app-config":
  "api.endpoint":
    url: https://api.example.com
```

  Key folding doesn't apply because `app-config` contains a hyphen and `api.endpoint` contains a dot.

#### Source Code Reference

```python  theme={null}
# toon_json_converter.py:281-290
class KeyFolder:
    SAFE_SEGMENT_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    @classmethod
    def can_fold(cls, key: str, value: Any, depth: int, max_depth: float) -> bool:
        return (
            depth 
  Output minified JSON without whitespace or indentation.

  **Default:** Pretty-printed with 2-space indentation

  **Applies to:** TOON → JSON and Folder → JSONL conversions

  **Source:** toon\_json\_converter.py:1228-1229

  **Data structure:** Sets `DecodeOptions.pretty = False`

#### Example: Pretty Output (Default)

**Input:** `data.toon`

```toon  theme={null}
name: Alice
age: 30
active: true
```

**Command:**

```bash  theme={null}
python toon_json_converter.py data.toon
```

**Output:** `data.json`

```json  theme={null}
{
  "name": "Alice",
  "age": 30,
  "active": true
}
```

#### Example: Compact Output

**Command:**

```bash  theme={null}
python toon_json_converter.py data.toon data.json --compact
```

**Output:** `data.json` (single line)

```json  theme={null}
{"name":"Alice","age":30,"active":true}
```

#### Use Cases

| Mode                 | Use Case                                                        |
| -------------------- | --------------------------------------------------------------- |
| **Pretty (default)** | Human-readable output, debugging, configuration files           |
| **Compact**          | Minimal file size, API responses, log files, machine processing |

### Indentation

  Set the number of spaces for JSON indentation.

  **Default:** `2`

  **Range:** Any positive integer

  **Ignored when:** Used with `--compact` flag

  **Source:** toon\_json\_converter.py:1232-1238

  **Data structure:** Sets `DecodeOptions.indent`

#### Example: Default 2-Space Indentation

**Command:**

```bash  theme={null}
python toon_json_converter.py data.toon data.json
```

**Output:**

```json  theme={null}
{
  "server": {
    "port": 8080
  }
}
```

#### Example: 4-Space Indentation

**Command:**

```bash  theme={null}
python toon_json_converter.py data.toon data.json --indent 4
```

**Output:**

```json  theme={null}
{
    "server": {
        "port": 8080
    }
}
```

#### Example: Tab Indentation

  The converter does not support tab character indentation via a flag. Use `--indent` with space count only.

To achieve tab indentation, you would need to post-process the output:

```bash  theme={null}
python toon_json_converter.py data.toon temp.json --indent 1
sed 's/ /\t/g' temp.json > data.json
```

### Path Expansion

  Expand dotted keys into nested objects during TOON → JSON conversion.

  **Default:** Disabled (per TOON spec §13.4)

  **Applies to:** Keys containing dots (`.`) without brackets

  **Source:** toon\_json\_converter.py:1230-1231

  **Data structure:** Sets `DecodeOptions.expand_paths = True`

  **Parser reference:** toon\_json\_converter.py:656-657, 713-716

#### Example: Without Path Expansion (Default)

**Input:** `config.toon`

```toon  theme={null}
server.host: localhost
server.port: 8080
server.ssl.enabled: true
```

**Command:**

```bash  theme={null}
python toon_json_converter.py config.toon
```

**Output:** `config.json`

```json  theme={null}
{
  "server.host": "localhost",
  "server.port": 8080,
  "server.ssl.enabled": true
}
```

  By default, dotted keys are treated as literal string keys, not nested paths.

#### Example: With Path Expansion

**Command:**

```bash  theme={null}
python toon_json_converter.py config.toon config.json --expand-paths
```

**Output:** `config.json`

```json  theme={null}
{
  "server": {
    "host": "localhost",
    "port": 8080,
    "ssl": {
      "enabled": true
    }
  }
}
```

#### Path Expansion Rules

**Expansion applies when:**

* ✅ Key contains dots (`.`)
* ✅ Key does NOT contain brackets (`[`, `]`)
* ✅ `--expand-paths` flag is set

**Expansion does NOT apply to:**

* ❌ Keys without dots
* ❌ Array notation like `items[0]`
* ❌ When `--expand-paths` is not set (default)

#### Example: Mixed Keys

**Input:** `mixed.toon`

```toon  theme={null}
app.name: MyApp
app.version: 2.0
metadata: {}
items[2]: a, b
```

**Command:**

```bash  theme={null}
python toon_json_converter.py mixed.toon --expand-paths
```

**Output:**

```json  theme={null}
{
  "app": {
    "name": "MyApp",
    "version": "2.0"
  },
  "metadata": {},
  "items": ["a", "b"]
}
```

  `items[2]` is NOT expanded because it contains brackets (array notation).

#### Source Code Reference

```python  theme={null}
# toon_json_converter.py:713-716
if "." in key and "[" not in key and self.expand_paths:
    self._set_nested_key(obj, key, value)
else:
    obj[key] = value
```

```python  theme={null}
# toon_json_converter.py:1005-1010
def _set_nested_key(self, obj: dict, key_path: str, value: Any) -> None:
    parts = key_path.split(".")
    current = obj
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = value
```

#### Complementary with Key Folding

`--key-folding` (encoding) and `--expand-paths` (decoding) are complementary:

**Round-trip example:**

```bash  theme={null}
# Start with nested JSON
echo '{"a":{"b":{"c":1}}}' > input.json

# Encode with key folding
python toon_json_converter.py input.json temp.toon --key-folding
# Result: a.b.c: 1

# Decode with path expansion
python toon_json_converter.py temp.toon output.json --expand-paths
# Result: {"a":{"b":{"c":1}}}

# Verify round-trip
diff input.json output.json  # Should be identical (ignoring whitespace)
```

### Combining Decoding Options

You can combine decoding options:

```bash  theme={null}
python toon_json_converter.py data.toon output.json --indent 4 --expand-paths
```

  Combining `--compact` with `--indent` will ignore the `--indent` value since compact mode removes all whitespace.

## Option Scope Summary

| Option            | Applies When                                       | Ignored When                                |
| ----------------- | -------------------------------------------------- | ------------------------------------------- |
| `--tab`           | Converting JSON/JSONL → TOON                       | Converting TOON → JSON                      |
| `--pipe`          | Converting JSON/JSONL → TOON                       | Converting TOON → JSON                      |
| `--length-marker` | Converting JSON/JSONL → TOON                       | Converting TOON → JSON                      |
| `--key-folding`   | Converting JSON/JSONL → TOON                       | Converting TOON → JSON                      |
| `--compact`       | Converting TOON → JSON/JSONL                       | Converting JSON → TOON                      |
| `--indent`        | Converting TOON → JSON/JSONL (without `--compact`) | Converting JSON → TOON, or with `--compact` |
| `--expand-paths`  | Converting TOON → JSON/JSONL                       | Converting JSON → TOON                      |

## Next Steps

  
    Learn batch processing workflows
  

  
    Understand all four conversion modes
  

  
    Complete CLI command reference
  

  
    Deep dive into TOON format specification