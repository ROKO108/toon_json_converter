> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# Batch Conversion

> Guide to processing multiple files efficiently with TOON JSON Converter

## Overview

The TOON JSON Converter includes built-in batch conversion capabilities for processing multiple files efficiently. This guide covers JSONL splitting, folder aggregation, and advanced batch processing techniques.

## Built-In Batch Modes

The converter provides two native batch conversion modes:

  
    Split a JSONL file into multiple TOON files
  

  
    Aggregate multiple TOON files into one JSONL file
  

## JSONL to TOON Folder

### Basic Usage

Convert each line in a JSONL file to a separate TOON file:

```bash  theme={null}
python toon_json_converter.py dataset.jsonl output_folder/
```

### File Naming Convention

Generated files follow this pattern: `{base_name}_{index:04d}.toon`

**Example:**

```bash  theme={null}
python toon_json_converter.py logs.jsonl logs_toons/
```

**Creates:**

```
logs_toons/
  logs_0000.toon
  logs_0001.toon
  logs_0002.toon
  ...
```

Source reference: `toon_json_converter.py:1113`

```python  theme={null}
output_file = os.path.join(output_dir, f"{base_name}_{i:04d}.toon")
```

### Automatic Output Folder

If output is omitted, creates `{input_name}_toons/` folder:

```bash  theme={null}
python toon_json_converter.py dataset.jsonl
# Creates: dataset_toons/
```

### Example: Processing Log Files

**Input:** `events.jsonl` (1,000 lines)

```jsonl  theme={null}
{"id": 1, "event": "login", "user": "alice", "timestamp": "2024-01-01T10:00:00Z"}
{"id": 2, "event": "purchase", "user": "bob", "amount": 49.99}
{"id": 3, "event": "logout", "user": "alice", "timestamp": "2024-01-01T10:30:00Z"}
...
```

**Command:**

```bash  theme={null}
python toon_json_converter.py events.jsonl events_toons/ --tab --length-marker
```

**Output:** 1,000 files in `events_toons/`

`events_0000.toon`:

```toon  theme={null}
id: 1
event: login
user: alice
timestamp: 2024-01-01T10:00:00Z
```

`events_0001.toon`:

```toon  theme={null}
id: 2
event: purchase
user: bob
amount: 49.99
```

**Terminal output:**

```
✅ Converted 1000 items to events_toons/
```

### Error Handling

The converter gracefully handles errors and continues processing:

**Input:** `mixed.jsonl`

```jsonl  theme={null}
{"valid": "data", "id": 1}
invalid json line here
{"valid": "data", "id": 2}
{"another": "malformed" json
{"valid": "data", "id": 3}
```

**Command:**

```bash  theme={null}
python toon_json_converter.py mixed.jsonl output/
```

**Terminal output:**

```
⚠️  Line 1: Invalid JSON: Expecting value: line 1 column 1 (char 0)
⚠️  Line 3: Invalid JSON: Expecting ',' delimiter: line 1 column 20 (char 19)
✅ Converted 3 items to output/
⚠️  2 items skipped due to errors
```

### Empty Lines

Empty or whitespace-only lines are automatically skipped:

**Input:** `sparse.jsonl`

```jsonl  theme={null}
{"id": 1}

{"id": 2}
   
{"id": 3}
```

**Result:** Creates only 3 files (empty lines ignored)

Source reference: `toon_json_converter.py:1107-1109`

```python  theme={null}
for i, raw_line in enumerate(f):
    line = raw_line.strip()
    if not line:
        continue
```

### Performance Considerations

**Processing 10,000-line JSONL file:**

```bash  theme={null}
time python toon_json_converter.py large_dataset.jsonl output/
```

**Typical performance:**

* **Small objects (less than 1KB):** \~5,000-10,000 records/second
* **Medium objects (around 10KB):** \~1,000-2,000 records/second
* **Large objects (greater than 100KB):** \~100-500 records/second

  Performance depends on object complexity, disk I/O speed, and system resources.

## TOON Folder to JSONL

### Basic Usage

Aggregate all TOON files in a folder into a single JSONL file:

```bash  theme={null}
python toon_json_converter.py input_folder/ output.jsonl
```

### File Processing Order

TOON files are processed in **alphabetical order** for deterministic output:

```bash  theme={null}
python toon_json_converter.py data_toons/ dataset.jsonl
```

**Processing order:**

```
data_toons/
  config_0003.toon  ← 1st (alphabetically)
  config_0010.toon  ← 2nd
  log_0001.toon     ← 3rd
  log_0002.toon     ← 4th
```

Source reference: `toon_json_converter.py:1124`

```python  theme={null}
toon_files = sorted(f for f in os.listdir(input_folder) if f.endswith(".toon"))
```

### Automatic Output Path

If output is omitted, creates `{folder_name}.jsonl`:

```bash  theme={null}
python toon_json_converter.py data_toons/
# Creates: data_toons.jsonl
```

### Example: Aggregating User Records

**Input folder:** `users/`

```
users/
  user_0000.toon
  user_0001.toon
  user_0002.toon
```

`user_0000.toon`:

```toon  theme={null}
id: 1
name: Alice
email: alice@example.com
roles[2]: admin, developer
```

`user_0001.toon`:

```toon  theme={null}
id: 2
name: Bob
email: bob@example.com
roles[1]: user
```

`user_0002.toon`:

```toon  theme={null}
id: 3
name: Carol
email: carol@example.com
roles[3]: admin, user, tester
```

**Command:**

```bash  theme={null}
python toon_json_converter.py users/ users.jsonl --compact
```

**Output:** `users.jsonl`

```jsonl  theme={null}
{"id":1,"name":"Alice","email":"alice@example.com","roles":["admin","developer"]}
{"id":2,"name":"Bob","email":"bob@example.com","roles":["user"]}
{"id":3,"name":"Carol","email":"carol@example.com","roles":["admin","user","tester"]}
```

**Terminal output:**

```
✅ Converted 3 items to users.jsonl
```

### Error Handling

The converter handles various error types:

#### File Read Errors

```
⚠️  locked.toon: File read error: [Errno 13] Permission denied: 'locked.toon'
```

#### Parse Errors

```
⚠️  corrupt.toon: Parse error: Invalid array header
```

#### Unexpected Errors

```
⚠️  data.toon: Unexpected error (UnicodeDecodeError): 'utf-8' codec can't decode byte
```

Source reference: `toon_json_converter.py:1136-1144`

```python  theme={null}
try:
    data = self.parser.parse(self._read_toon(toon_path))
    outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
    result.record_success()
except OSError as e:
    result.record_error(f"{toon_file}: File read error", e)
except (ValueError, KeyError) as e:
    result.record_error(f"{toon_file}: Parse error", e)
except Exception as e:
    result.record_error(f"{toon_file}: Unexpected error ({type(e).__name__})", e)
```

### Empty Folder Handling

If no `.toon` files are found:

```bash  theme={null}
python toon_json_converter.py empty_folder/ output.jsonl
```

**Terminal output:**

```
⚠️  No .toon files found in empty_folder/
```

Source reference: `toon_json_converter.py:1125-1127`

```python  theme={null}
if not toon_files:
    print(f"⚠️  No .toon files found in {input_folder}")
    return
```

### Mixed File Types

Only `.toon` files are processed; other files are ignored:

**Folder structure:**

```
data/
  record_0001.toon  ← Processed
  record_0002.toon  ← Processed
  readme.txt        ← Ignored
  config.json       ← Ignored
  image.png         ← Ignored
```

**Result:** Only `record_0001.toon` and `record_0002.toon` are converted.

## Advanced Batch Processing

### Shell Scripting

Process multiple files using shell loops:

#### Convert Multiple JSON Files

```bash  theme={null}
#!/bin/bash
for file in data/*.json; do
  python toon_json_converter.py "$file" --tab --length-marker
done
```

#### Convert with Custom Output Names

```bash  theme={null}
#!/bin/bash
for file in inputs/*.json; do
  base=$(basename "$file" .json)
  python toon_json_converter.py "$file" "outputs/${base}.toon" --pipe
done
```

#### Parallel Processing with xargs

```bash  theme={null}
find data/ -name "*.json" | xargs -I {} -P 4 python toon_json_converter.py {} --tab
```

  `-P 4` runs 4 conversions in parallel. Adjust based on CPU cores.

### Python Scripting

Use the converter programmatically:

```python  theme={null}
#!/usr/bin/env python3
import os
from toon_json_converter import BidirectionalConverter, EncodeOptions, Delimiter

# Configure options
options = EncodeOptions(
    delimiter=Delimiter.TAB,
    length_marker=True,
    key_folding=True
)

converter = BidirectionalConverter(encode_options=options)

# Batch convert all JSON files
input_dir = "data/json"
output_dir = "data/toon"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".json", ".toon"))
        
        try:
            converter.convert_file(input_path, output_path)
        except Exception as e:
            print(f"❌ Failed to convert {filename}: {e}")

print("\n✅ Batch conversion complete!")
```

### Directory Structure Preservation

Preserve directory hierarchy during batch conversion:

```bash  theme={null}
#!/bin/bash

# Find all JSON files recursively
find source/ -name "*.json" | while read -r file; do
  # Calculate relative path
  rel_path="${file#source/}"
  output_path="output/${rel_path%.json}.toon"
  
  # Create output directory
  mkdir -p "$(dirname "$output_path")"
  
  # Convert
  python toon_json_converter.py "$file" "$output_path" --tab
done
```

**Example structure:**

```
source/                      output/
  users/                      users/
    admin.json        →         admin.toon
    guest.json        →         guest.toon
  config/                     config/
    server.json       →         server.toon
    database.json     →         database.toon
```

### Batch Processing with Filtering

Convert only files matching specific criteria:

```bash  theme={null}
#!/bin/bash

# Convert only files larger than 1KB
find data/ -name "*.json" -size +1k | while read -r file; do
  python toon_json_converter.py "$file" --tab
done
```

```bash  theme={null}
# Convert only recently modified files (last 7 days)
find data/ -name "*.json" -mtime -7 | while read -r file; do
  python toon_json_converter.py "$file"
done
```

### Progress Tracking

Add progress indicators for large batches:

```bash  theme={null}
#!/bin/bash

files=(data/*.json)
total=${#files[@]}
current=0

for file in "${files[@]}"; do
  ((current++))
  echo "[$current/$total] Converting $file..."
  python toon_json_converter.py "$file" --tab
done

echo "✅ Converted $total files"
```

**Output:**

```
[1/50] Converting data/file1.json...
✅ data/file1.json → data/file1.toon
[2/50] Converting data/file2.json...
✅ data/file2.json → data/file2.toon
...
✅ Converted 50 files
```

## Error Handling Strategies

### Logging Errors to File

```bash  theme={null}
#!/bin/bash

error_log="conversion_errors.log"
: > "$error_log"  # Clear log file

for file in data/*.json; do
  if ! python toon_json_converter.py "$file" 2>> "$error_log"; then
    echo "Failed: $file" >> "$error_log"
  fi
done

if [ -s "$error_log" ]; then
  echo "⚠️  Errors occurred. See $error_log"
else
  echo "✅ All conversions successful"
fi
```

### Skip vs. Halt on Error

**Skip errors (continue processing):**

```bash  theme={null}
for file in data/*.json; do
  python toon_json_converter.py "$file" || echo "⚠️  Skipped $file"
done
```

**Halt on first error:**

```bash  theme={null}
for file in data/*.json; do
  python toon_json_converter.py "$file" || exit 1
done
```

### Retry Failed Conversions

```bash  theme={null}
#!/bin/bash

max_retries=3

for file in data/*.json; do
  success=false
  
  for ((i=1; i
  
    Apply the same options across all files in a batch for consistent output:

    ```bash  theme={null}
    # Good: Consistent options
    for file in *.json; do
      python toon_json_converter.py "$file" --tab --length-marker
    done
    ```

    ```bash  theme={null}
    # Bad: Inconsistent options
    python toon_json_converter.py file1.json --tab
    python toon_json_converter.py file2.json --pipe
    python toon_json_converter.py file3.json  # defaults
    ```
  

  
    Verify conversions by round-tripping:

    ```bash  theme={null}
    # Convert JSON → TOON → JSON and compare
    python toon_json_converter.py original.json temp.toon
    python toon_json_converter.py temp.toon reconstructed.json
    diff 

  
    For very large JSONL files (>1GB), consider splitting first:

    ```bash  theme={null}
    # Split into 10,000-line chunks
    split -l 10000 huge_file.jsonl chunk_

    # Convert each chunk
    for chunk in chunk_*; do
      python toon_json_converter.py "$chunk" "${chunk}_toons/"
    done
    ```
  

  
    Track batch conversion scripts in version control:

    ```bash  theme={null}
    git add batch_convert.sh
    git commit -m "Add batch conversion script with tab delimiter"
    ```
  

  
    Check available disk space before large batch operations:

    ```bash  theme={null}
    # Estimate output size (TOON is typically 1.1-1.3x JSON size)
    input_size=$(du -sb data/*.json | awk '{sum+=$1} END {print sum}')
    required_space=$((input_size * 13 / 10))  # 1.3x
    available_space=$(df -B1 . | tail -1 | awk '{print $4}')

    if [ $required_space -gt $available_space ]; then
      echo "❌ Insufficient disk space"
      exit 1
    fi
    ```
  

## Real-World Examples

### Example 1: Processing API Responses

```bash  theme={null}
#!/bin/bash
# Convert API response logs from JSONL to individual TOON files

input="api_responses.jsonl"
output_dir="responses_$(date +%Y%m%d)"

python toon_json_converter.py "$input" "$output_dir/" --tab --length-marker

echo "✅ Converted API responses to $output_dir/"
```

### Example 2: Aggregating Configuration Files

```bash  theme={null}
#!/bin/bash
# Aggregate all service configs into a single JSONL file

configs_dir="configs/services"
output="all_configs_$(date +%Y%m%d).jsonl"

python toon_json_converter.py "$configs_dir/" "$output" --compact

echo "✅ Aggregated configs to $output"
```

### Example 3: Data Pipeline

```bash  theme={null}
#!/bin/bash
# Multi-stage data processing pipeline

# Stage 1: Extract data (assume this generates raw.jsonl)
./extract_data.sh > raw.jsonl

# Stage 2: Split into individual TOON files for manual review
python toon_json_converter.py raw.jsonl review_toons/ --tab

echo "📝 Review files in review_toons/ and make edits"
read -p "Press Enter when ready to continue..."

# Stage 3: Aggregate back to JSONL
python toon_json_converter.py review_toons/ processed.jsonl --compact

# Stage 4: Load into database (assume this consumes JSONL)
./load_to_db.sh processed.jsonl

echo "✅ Pipeline complete"
```

## Next Steps

  
    Complete command-line interface reference
  

  
    Deep dive into all options
  

  
    Learn about all conversion modes
  

  
    Understand the TOON format specification