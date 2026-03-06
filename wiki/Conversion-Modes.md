> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# Conversion Modes

> Detailed guide to all four conversion modes supported by TOON JSON Converter

## Overview

The TOON JSON Converter automatically detects the conversion direction based on file extensions, supporting four bidirectional conversion modes:

  
    Single file conversion from JSON to TOON format
  

  
    Batch conversion from JSONL to multiple TOON files
  

  
    Single file conversion from TOON to JSON format
  

  
    Batch conversion from multiple TOON files to JSONL
  

## Mode 1: JSON → TOON

Convert a single JSON file to TOON format.

### Basic Usage

```bash  theme={null}
python toon_json_converter.py input.json output.toon
```

### Automatic Output Path

If you omit the output path, it automatically generates `input.toon`:

```bash  theme={null}
python toon_json_converter.py data.json
# Creates: data.toon
```

### Example Conversion

**Input:** `users.json`

```json  theme={null}
{
  "users": [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
  ]
}
```

**Command:**

```bash  theme={null}
python toon_json_converter.py users.json
```

**Output:** `users.toon`

```toon  theme={null}
users[2]{name,age}:
  Alice, 30
  Bob, 25
```

**Terminal output:**

```
✅ users.json → users.toon
```

### With Options

```bash  theme={null}
python toon_json_converter.py users.json users.toon --tab --length-marker
```

**Output:** `users.toon`

```toon  theme={null}
users[#2 ]{name,age}:
  Alice	30
  Bob	25
```

### Implementation Details

Source code reference: `toon_json_converter.py:1084-1088`

```python  theme={null}
def _convert_json_to_toon(self, input_path: str, output_path: str) -> None:
    data = self._read_json(input_path)
    toon_content = self.encoder.encode(data)
    self._write_toon(output_path, toon_content)
    print(f"✅ {input_path} → {output_path}")
```

## Mode 2: JSONL → TOON Folder

Convert each line in a JSONL file to a separate TOON file in a folder.

### Basic Usage

```bash  theme={null}
python toon_json_converter.py input.jsonl output_folder/
```

### Automatic Output Path

If you omit the output path, it creates a folder named `{filename}_toons`:

```bash  theme={null}
python toon_json_converter.py dataset.jsonl
# Creates folder: dataset_toons/
```

### Example Conversion

**Input:** `logs.jsonl`

```jsonl  theme={null}
{"timestamp": "2024-01-01", "level": "INFO", "message": "Server started"}
{"timestamp": "2024-01-01", "level": "ERROR", "message": "Connection failed"}
{"timestamp": "2024-01-02", "level": "INFO", "message": "Request processed"}
```

**Command:**

```bash  theme={null}
python toon_json_converter.py logs.jsonl
```

**Output:** Creates folder `logs_toons/` with three files:

`logs_0000.toon`:

```toon  theme={null}
timestamp: 2024-01-01
level: INFO
message: "Server started"
```

`logs_0001.toon`:

```toon  theme={null}
timestamp: 2024-01-01
level: ERROR
message: "Connection failed"
```

`logs_0002.toon`:

```toon  theme={null}
timestamp: 2024-01-02
level: INFO
message: "Request processed"
```

**Terminal output:**

```
✅ Converted 3 items to logs_toons/
```

### File Naming Convention

Files are named using the pattern: `{base_name}_{index:04d}.toon`

* `base_name`: Original filename without extension
* `index`: Zero-padded 4-digit index (0000, 0001, 0002, ...)

### Error Handling

The converter skips invalid lines and reports errors:

**Input:** `mixed.jsonl`

```jsonl  theme={null}
{"valid": "data"}
invalid json line
{"more": "valid data"}
```

**Terminal output:**

```
⚠️  Line 1: Invalid JSON: Expecting value: line 1 column 1 (char 0)
✅ Converted 2 items to mixed_toons/
⚠️  1 items skipped due to errors
```

### Implementation Details

Source code reference: `toon_json_converter.py:1100-1121`

The converter:

1. Creates the output directory if it doesn't exist
2. Processes each non-empty line
3. Generates sequential filenames with zero-padding
4. Reports success count and any errors

## Mode 3: TOON → JSON

Convert a single TOON file to JSON format.

### Basic Usage

```bash  theme={null}
python toon_json_converter.py input.toon output.json
```

### Automatic Output Path

If you omit the output path, it automatically generates `input.json`:

```bash  theme={null}
python toon_json_converter.py data.toon
# Creates: data.json
```

### Example Conversion

**Input:** `config.toon`

```toon  theme={null}
server:
  host: localhost
  port: 8080
  features[3]: ssl, compression, logging
database:
  url: "postgresql://localhost/mydb"
  pool_size: 10
```

**Command:**

```bash  theme={null}
python toon_json_converter.py config.toon
```

**Output:** `config.json`

```json  theme={null}
{
  "server": {
    "host": "localhost",
    "port": 8080,
    "features": ["ssl", "compression", "logging"]
  },
  "database": {
    "url": "postgresql://localhost/mydb",
    "pool_size": 10
  }
}
```

**Terminal output:**

```
✅ config.toon → config.json
```

### With Options

#### Compact Output

```bash  theme={null}
python toon_json_converter.py config.toon config.json --compact
```

**Output:** `config.json` (single line)

```json  theme={null}
{"server":{"host":"localhost","port":8080,"features":["ssl","compression","logging"]},"database":{"url":"postgresql://localhost/mydb","pool_size":10}}
```

#### Custom Indentation

```bash  theme={null}
python toon_json_converter.py config.toon config.json --indent 4
```

**Output:** `config.json`

```json  theme={null}
{
    "server": {
        "host": "localhost",
        "port": 8080
    }
}
```

#### Expand Dotted Paths

**Input:** `dotted.toon`

```toon  theme={null}
app.config.debug: true
app.config.port: 3000
```

**Command:**

```bash  theme={null}
python toon_json_converter.py dotted.toon --expand-paths
```

**Output:** `dotted.json`

```json  theme={null}
{
  "app": {
    "config": {
      "debug": true,
      "port": 3000
    }
  }
}
```

### Implementation Details

Source code reference: `toon_json_converter.py:1090-1094`

```python  theme={null}
def _convert_toon_to_json(self, input_path: str, output_path: str) -> None:
    toon_content = self._read_toon(input_path)
    data = self.parser.parse(toon_content)
    self._write_json(output_path, data)
    print(f"✅ {input_path} → {output_path}")
```

## Mode 4: TOON Folder → JSONL

Convert all TOON files in a folder to a single JSONL file.

### Basic Usage

```bash  theme={null}
python toon_json_converter.py input_folder/ output.jsonl
```

### Automatic Output Path

If you omit the output path, it creates `{folder_name}.jsonl`:

```bash  theme={null}
python toon_json_converter.py data_toons/
# Creates: data_toons.jsonl
```

### Example Conversion

**Input folder:** `events/`

```
events/
  event_0000.toon
  event_0001.toon
  event_0002.toon
```

`event_0000.toon`:

```toon  theme={null}
type: login
user: alice
timestamp: 1704067200
```

`event_0001.toon`:

```toon  theme={null}
type: purchase
user: bob
amount: 49.99
```

`event_0002.toon`:

```toon  theme={null}
type: logout
user: alice
timestamp: 1704070800
```

**Command:**

```bash  theme={null}
python toon_json_converter.py events/
```

**Output:** `events.jsonl`

```jsonl  theme={null}
{"type":"login","user":"alice","timestamp":1704067200}
{"type":"purchase","user":"bob","amount":49.99}
{"type":"logout","user":"alice","timestamp":1704070800}
```

**Terminal output:**

```
✅ Converted 3 items to events.jsonl
```

### File Processing Order

TOON files are processed in **alphabetical order** (via `sorted()`). This ensures deterministic output.

Source code reference: `toon_json_converter.py:1124`

```python  theme={null}
toon_files = sorted(f for f in os.listdir(input_folder) if f.endswith(".toon"))
```

### Error Handling

The converter skips invalid files and reports errors:

**Terminal output example:**

```
⚠️  corrupt.toon: Parse error: Invalid array header
✅ Converted 5 items to output.jsonl
⚠️  1 items skipped due to errors
```

### Empty Folder Handling

If the folder contains no `.toon` files:

```bash  theme={null}
python toon_json_converter.py empty_folder/
```

**Terminal output:**

```
⚠️  No .toon files found in empty_folder/
```

### Implementation Details

Source code reference: `toon_json_converter.py:1123-1146`

The converter:

1. Scans for all `.toon` files in the directory
2. Sorts files alphabetically for consistent output
3. Parses each TOON file and writes as a single JSON line
4. Handles various error types (file read, parse, unexpected)
5. Reports summary with success/error counts

## Mode Detection Logic

The converter automatically detects the mode using this logic:

Source code reference: `toon_json_converter.py:1060-1078`

```python  theme={null}
if os.path.isdir(input_path):
    # Mode 4: Folder → JSONL
    output_path = output_path or f"{os.path.basename(input_path.rstrip('/'))}.jsonl"
    self._convert_folder_to_jsonl(input_path, output_path)
elif input_path.endswith(".jsonl"):
    # Mode 2: JSONL → Folder
    output_path = output_path or f"{os.path.splitext(os.path.basename(input_path))[0]}_toons"
    self._convert_jsonl_to_toon(input_path, output_path)
elif input_path.endswith(".json"):
    # Mode 1: JSON → TOON
    output_path = output_path or os.path.splitext(input_path)[0] + ".toon"
    self._convert_json_to_toon(input_path, output_path)
elif input_path.endswith(".toon"):
    # Mode 3: TOON → JSON
    output_path = output_path or os.path.splitext(input_path)[0] + ".json"
    self._convert_toon_to_json(input_path, output_path)
else:
    raise ValueError(f"Unsupported file type: {input_path}")
```

## Comparison Matrix

| Mode                  | Input                   | Output                  | Use Case                                               |
| --------------------- | ----------------------- | ----------------------- | ------------------------------------------------------ |
| **1. JSON → TOON**    | Single `.json` file     | Single `.toon` file     | Convert one JSON file to human-readable format         |
| **2. JSONL → Folder** | Single `.jsonl` file    | Folder of `.toon` files | Split a line-delimited JSON file into separate records |
| **3. TOON → JSON**    | Single `.toon` file     | Single `.json` file     | Convert TOON to machine-readable JSON                  |
| **4. Folder → JSONL** | Folder of `.toon` files | Single `.jsonl` file    | Aggregate multiple TOON files into one dataset         |

## Next Steps

  
    Learn about all command-line options in detail
  

  
    Master batch processing workflows
  

  
    Complete command-line interface reference
  

  
    Understand the TOON format specification