> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# CLI Reference

> Complete command-line interface reference for TOON JSON Converter

## Overview

The TOON JSON Converter provides a simple command-line interface that automatically detects the conversion direction based on file extensions.

## Basic Syntax

```bash  theme={null}
python toon_json_converter.py  [output] [options]
```

  Input file or folder path. The file extension determines the conversion direction:

  * `.json` - Converts to TOON format
  * `.jsonl` - Converts to folder of TOON files
  * `.toon` - Converts to JSON format
  * `folder/` - Converts all TOON files to JSONL

  Output file or folder path. If omitted, automatically generates output path based on input:

  * `data.json` → `data.toon`
  * `data.jsonl` → `data_toons/`
  * `data.toon` → `data.json`
  * `data_folder/` → `data_folder.jsonl`

## Conversion Modes

The converter supports four bidirectional conversion modes:

### 1. JSON to TOON

```bash  theme={null}
python toon_json_converter.py input.json output.toon
```

Converts a single JSON file to TOON format.

### 2. JSONL to TOON Folder

```bash  theme={null}
python toon_json_converter.py input.jsonl output_folder/
```

Converts each line in a JSONL file to a separate TOON file in a folder.

### 3. TOON to JSON

```bash  theme={null}
python toon_json_converter.py input.toon output.json
```

Converts a single TOON file to JSON format.

### 4. TOON Folder to JSONL

```bash  theme={null}
python toon_json_converter.py input_folder/ output.jsonl
```

Converts all TOON files in a folder to a single JSONL file.

## Command-Line Options

### General Options

  Specify output file or folder path. Alternative to using positional argument.

  ```bash  theme={null}
  python toon_json_converter.py data.json -o output.toon
  python toon_json_converter.py data.toon --output result.json
  ```

### Encoding Options (JSON → TOON)

These options apply when converting FROM JSON or JSONL TO TOON:

  Use tab (`\t`) as the delimiter for tabular arrays instead of comma.

  **Default:** Comma (`,`)

  **Line reference:** toon\_json\_converter.py:1215-1216

  ```bash  theme={null}
  python toon_json_converter.py data.json data.toon --tab
  ```

  **Example output:**

  ```toon  theme={null}
  users[3 ]{name,age}:
    Alice\t30
    Bob\t25
    Carol\t35
  ```

  Use pipe (`|`) as the delimiter for tabular arrays instead of comma.

  **Default:** Comma (`,`)

  **Line reference:** toon\_json\_converter.py:1217-1218

  ```bash  theme={null}
  python toon_json_converter.py data.json data.toon --pipe
  ```

  **Example output:**

  ```toon  theme={null}
  users[3|]{name,age}:
    Alice|30
    Bob|25
    Carol|35
  ```

  Add `#` prefix to array lengths in headers for improved readability.

  **Default:** No prefix

  **Line reference:** toon\_json\_converter.py:1219-1220

  ```bash  theme={null}
  python toon_json_converter.py data.json data.toon --length-marker
  ```

  **Example output:**

  ```toon  theme={null}
  items[#5]: apple, banana, cherry, date, fig
  ```

  Enable key folding for nested single-key objects. Converts chains like `{"a": {"b": {"c": value}}}` to `a.b.c: value`.

  **Default:** Disabled

  **Line reference:** toon\_json\_converter.py:1221-1222

  **Requirements:** Keys must match pattern `[A-Za-z_][A-Za-z0-9_]*`

  ```bash  theme={null}
  python toon_json_converter.py data.json data.toon --key-folding
  ```

  **Example transformation:**

  ```json  theme={null}
  {"server": {"config": {"port": 8080}}}
  ```

  Becomes:

  ```toon  theme={null}
  server.config.port: 8080
  ```

### Decoding Options (TOON → JSON)

These options apply when converting FROM TOON TO JSON or JSONL:

  Output minified JSON without whitespace or indentation.

  **Default:** Pretty-printed with 2-space indentation

  **Line reference:** toon\_json\_converter.py:1228-1229

  ```bash  theme={null}
  python toon_json_converter.py data.toon data.json --compact
  ```

  **Example output:**

  ```json  theme={null}
  {"name":"Alice","age":30,"active":true}
  ```

  Set the number of spaces for JSON indentation.

  **Default:** `2`

  **Line reference:** toon\_json\_converter.py:1232-1238

  ```bash  theme={null}
  python toon_json_converter.py data.toon data.json --indent 4
  ```

  **Example output:**

  ```json  theme={null}
  {
      "name": "Alice",
      "age": 30
  }
  ```

  Expand dotted keys into nested objects during TOON → JSON conversion.

  **Default:** Disabled (per TOON spec §13.4)

  **Line reference:** toon\_json\_converter.py:1230-1231

  ```bash  theme={null}
  python toon_json_converter.py data.toon data.json --expand-paths
  ```

  **Example transformation:**

  TOON input:

  ```toon  theme={null}
  server.config.port: 8080
  server.config.host: localhost
  ```

  Without `--expand-paths` (default):

  ```json  theme={null}
  {
    "server.config.port": 8080,
    "server.config.host": "localhost"
  }
  ```

  With `--expand-paths`:

  ```json  theme={null}
  {
    "server": {
      "config": {
        "port": 8080,
        "host": "localhost"
      }
    }
  }
  ```

## Exit Codes

The converter returns the following exit codes:

| Code | Meaning                                                     |
| ---- | ----------------------------------------------------------- |
| `0`  | Success                                                     |
| `1`  | Error (missing arguments, file not found, conversion error) |

## Examples

### Convert with Custom Delimiter

```bash  theme={null}
python toon_json_converter.py data.json data.toon --tab --length-marker
```

### Convert with Multiple Options

```bash  theme={null}
python toon_json_converter.py data.json output.toon --pipe --key-folding --length-marker
```

### Convert to Compact JSON

```bash  theme={null}
python toon_json_converter.py data.toon data.json --compact
```

### Batch Convert with Custom Output

```bash  theme={null}
python toon_json_converter.py dataset.jsonl -o toon_files/ --tab
```

## Help Command

Run the converter without arguments to display usage information:

```bash  theme={null}
python toon_json_converter.py
```

**Output:**

```
Bidirectional TOON ↔ JSON/JSONL Converter

Usage: python toon_json_converter.py  [output] [options]

Automatic direction detection:
  .json file      → .toon file
  .jsonl file     → folder of .toon files
  .toon file      → .json file
  folder of .toon → .jsonl file

Options:
  -o, --output    Output file/folder path

  Encoding options (JSON → TOON):
    --tab               Use tab delimiter
    --pipe              Use pipe delimiter
    --length-marker     Add # prefix to array lengths
    --key-folding       Enable key folding for nested objects

  Decoding options (TOON → JSON):
    --compact           Minified JSON output
    --indent         Set indentation spaces (default: 2)
    --expand-paths      Expand dotted keys into nested objects (§13.4, off by default)
```

## Next Steps

  
    Learn about all four conversion modes in detail
  

  
    Deep dive into all command-line options
  

  
    Process multiple files efficiently
  

  
    Get started with basic examples