> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# Quick Start

> Convert between JSON and TOON formats in minutes with practical examples

Get started with TOON JSON Converter by following these quick examples. The converter automatically detects the conversion direction based on file extensions.

## Your First Conversion

  
    Create a file called `example.json` with some sample data:

    ```json example.json theme={null}
    {
      "name": "Alice",
      "age": 30,
      "active": true,
      "scores": [95, 87, 92],
      "address": {
        "city": "Portland",
        "state": "OR"
      }
    }
    ```
  

  
    Run the converter:

    ```bash  theme={null}
    python toon_json_converter.py example.json
    ```

    This creates `example.toon` with the following content:

    ```toon example.toon theme={null}
    name: Alice
    age: 30
    active: true
    scores[3]: 95,87,92
    address:
      city: Portland
      state: OR
    ```

    
      Notice how the array `[95, 87, 92]` is represented as `scores[3]: 95,87,92` - the `[3]` indicates the array length.
    
  

  
    Now convert the TOON file back to JSON:

    ```bash  theme={null}
    python toon_json_converter.py example.toon output.json
    ```

    The `output.json` file will contain the original JSON structure, pretty-printed by default.
  

## Tabular Data Example

TOON format excels at representing tabular data. Here's how arrays of objects are handled:

  ```json input.json theme={null}
  {
    "users": [
      {"id": 1, "name": "Alice", "role": "admin"},
      {"id": 2, "name": "Bob", "role": "user"},
      {"id": 3, "name": "Carol", "role": "user"}
    ]
  }
  ```

  ```toon output.toon theme={null}
  users[3]{id,name,role}:
    1,Alice,admin
    2,Bob,user
    3,Carol,"user"
  ```

Convert it:

```bash  theme={null}
python toon_json_converter.py input.json output.toon
```

  The header `users[3]{id,name,role}:` tells the parser:

  * `[3]` - array has 3 items
  * `{id,name,role}` - each object has these fields in this order
  * Data rows follow with comma-separated values

## Batch Conversion

### JSONL to Multiple TOON Files

Convert a JSONL (JSON Lines) file where each line is a separate JSON object:

```bash  theme={null}
python toon_json_converter.py data.jsonl toon_output/
```

This creates a folder `toon_output/` with files like:

* `data_0000.toon`
* `data_0001.toon`
* `data_0002.toon`

### Folder of TOON Files to JSONL

Convert multiple TOON files back to a single JSONL file:

```bash  theme={null}
python toon_json_converter.py toon_output/ combined.jsonl
```

## Conversion Options

Customize your conversions with command-line options:

### Encoding Options (JSON → TOON)

  ```bash Tab Delimiter theme={null}
  python toon_json_converter.py data.json data.toon --tab
  ```

  ```bash Pipe Delimiter theme={null}
  python toon_json_converter.py data.json data.toon --pipe
  ```

  ```bash Length Marker theme={null}
  python toon_json_converter.py data.json data.toon --length-marker
  # Arrays will be [#3] instead of [3]
  ```

  ```bash Key Folding theme={null}
  python toon_json_converter.py data.json data.toon --key-folding
  # Nested single-key objects become: outer.inner.leaf: value
  ```

### Decoding Options (TOON → JSON)

  ```bash Compact JSON theme={null}
  python toon_json_converter.py data.toon data.json --compact
  # No indentation, single-line output
  ```

  ```bash Custom Indentation theme={null}
  python toon_json_converter.py data.toon data.json --indent 4
  # Use 4 spaces instead of default 2
  ```

  ```bash Expand Paths theme={null}
  python toon_json_converter.py data.toon data.json --expand-paths
  # Converts dotted keys like "a.b.c" into nested objects
  ```

## Using in Python Code

You can also use the converter programmatically:

```python  theme={null}
from toon_json_converter import (
    BidirectionalConverter,
    EncodeOptions,
    DecodeOptions,
    Delimiter
)

# Configure encoding options
encode_opts = EncodeOptions(
    indent_size=2,
    delimiter=Delimiter.COMMA,
    length_marker=False,
    key_folding=True
)

# Configure decoding options
decode_opts = DecodeOptions(
    pretty=True,
    indent=2,
    expand_paths=False
)

# Create converter
converter = BidirectionalConverter(encode_opts, decode_opts)

# Convert files automatically
converter.convert_file("input.json", "output.toon")
converter.convert_file("input.toon", "output.json")
```

### Direct Encoding/Decoding

For working with data in memory:

```python  theme={null}
from toon_json_converter import TOONEncoder, TOONParser
import json

# Encode Python data to TOON string
encoder = TOONEncoder()
data = {"name": "Alice", "scores": [95, 87, 92]}
toon_string = encoder.encode(data)
print(toon_string)
# Output:
# name: Alice
# scores[3]: 95,87,92

# Parse TOON string to Python data
parser = TOONParser()
toon_content = """name: Alice
scores[3]: 95,87,92"""
result = parser.parse(toon_content)
print(json.dumps(result, indent=2))
# Output:
# {
#   "name": "Alice",
#   "scores": [95, 87, 92]
# }
```

## Common Patterns

### Primitive Arrays

Arrays of simple values (strings, numbers, booleans) are written inline:

```toon  theme={null}
tags[4]: python,converter,json,toon
numbers[5]: 1,2,3,4,5
flags[3]: true,false,true
```

### Nested Objects

Objects can be nested naturally:

```toon  theme={null}
config:
  database:
    host: localhost
    port: 5432
  cache:
    enabled: true
    ttl: 3600
```

### List of Objects

Arrays containing non-uniform objects or nested structures:

```toon  theme={null}
items[2]:
  - name: Item 1
    tags[2]: new,featured
  - name: Item 2
    tags[1]: sale
```

## Next Steps

  
    Explore all encoding and decoding options
  

  
    Learn the TOON format specification
  

  
    Browse the complete API documentation
  

  
    See more real-world examples