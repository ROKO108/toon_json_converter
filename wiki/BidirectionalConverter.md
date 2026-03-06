> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# BidirectionalConverter

> High-level converter for bidirectional TOON ↔ JSON file conversion

The `BidirectionalConverter` class provides a high-level interface for converting files between TOON and JSON formats. It automatically detects the conversion direction based on file extensions and handles batch conversions.

## Constructor

```python  theme={null}
BidirectionalConverter(
    encode_options: EncodeOptions | None = None,
    decode_options: DecodeOptions | None = None
)
```

  Configuration options for JSON → TOON encoding. If not provided, uses default [[EncodeOptions]].

  Configuration options for TOON → JSON decoding. If not provided, uses default [[DecodeOptions]].

### Example

```python  theme={null}
from toon_json_converter import (
    BidirectionalConverter,
    EncodeOptions,
    DecodeOptions,
    Delimiter
)

# Create converter with custom options
converter = BidirectionalConverter(
    encode_options=EncodeOptions(
        delimiter=Delimiter.TAB,
        key_folding=True
    ),
    decode_options=DecodeOptions(
        pretty=True,
        indent=4
    )
)
```

## Methods

### convert\_file

Convert files automatically detecting direction from file extension.

```python  theme={null}
converter.convert_file(
    input_path: str,
    output_path: str | None = None
) -> None
```

  Path to the input file or directory. Supported inputs:

  * `.json` file → converts to `.toon`
  * `.jsonl` file → converts to folder of `.toon` files
  * `.toon` file → converts to `.json`
  * Directory of `.toon` files → converts to `.jsonl`

  Path for the output file or directory. If not provided, generates an output path based on the input filename.

  Raised if the input file type is not supported.

  Raised if file read/write operations fail.

## Usage Examples

### Single File Conversion

```python  theme={null}
from toon_json_converter import BidirectionalConverter

converter = BidirectionalConverter()

# JSON to TOON
converter.convert_file("data.json", "data.toon")
# Output: ✅ data.json → data.toon

# TOON to JSON
converter.convert_file("data.toon", "data.json")
# Output: ✅ data.toon → data.json
```

### Automatic Output Path

If you don't specify an output path, it will be generated automatically:

```python  theme={null}
# Converts data.json → data.toon
converter.convert_file("data.json")

# Converts data.toon → data.json
converter.convert_file("data.toon")
```

### Batch Conversion: JSONL to TOON Files

Convert a JSONL file (one JSON object per line) into a directory of TOON files:

```python  theme={null}
converter.convert_file("dataset.jsonl", "dataset_toons/")
# Output:
# ✅ Converted 150 items to dataset_toons/
# Creates: dataset_0000.toon, dataset_0001.toon, ...
```

Each line in the JSONL file becomes a separate `.toon` file with a zero-padded numeric suffix.

### Batch Conversion: TOON Directory to JSONL

Convert a directory of TOON files into a single JSONL file:

```python  theme={null}
converter.convert_file("dataset_toons/", "dataset.jsonl")
# Output:
# ✅ Converted 150 items to dataset.jsonl
```

All `.toon` files in the directory are sorted alphabetically and converted to JSON objects, one per line.

### Custom Encoding Options

```python  theme={null}
from toon_json_converter import (
    BidirectionalConverter,
    EncodeOptions,
    Delimiter
)

# Use tabs as delimiters and enable length markers
converter = BidirectionalConverter(
    encode_options=EncodeOptions(
        delimiter=Delimiter.TAB,
        length_marker=True
    )
)

data = {
    "users": [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
}

converter.convert_file("users.json", "users.toon")
```

Output in `users.toon`:

```
users[#2 ]{name,age}:
  Alice  30
  Bob    25
```

### Custom Decoding Options

```python  theme={null}
from toon_json_converter import (
    BidirectionalConverter,
    DecodeOptions
)

# Compact JSON output without pretty printing
converter = BidirectionalConverter(
    decode_options=DecodeOptions(
        pretty=False
    )
)

converter.convert_file("data.toon", "data.json")
# Produces minified JSON output
```

## Supported Conversions

| Input     | Output    | Description                                      |
| --------- | --------- | ------------------------------------------------ |
| `.json`   | `.toon`   | Single JSON file to single TOON file             |
| `.jsonl`  | Directory | JSONL to multiple TOON files (one per line)      |
| `.toon`   | `.json`   | Single TOON file to single JSON file             |
| Directory | `.jsonl`  | Multiple TOON files to JSONL (one line per file) |

## Error Handling

The converter provides informative error messages:

```python  theme={null}
try:
    converter.convert_file("missing.json")
except ValueError as e:
    print(f"Conversion error: {e}")
except OSError as e:
    print(f"File system error: {e}")
```

For batch conversions, errors are reported but don't stop the entire process:

```
✅ Converted 148 items to output/
⚠️  2 items skipped due to errors
```

## Internal Components

The `BidirectionalConverter` internally uses:

* **[[TOONEncoder]]** - For JSON → TOON conversion
* **[[TOONParser]]** - For TOON → JSON conversion

If you need more control over the conversion process, you can use these classes directly.