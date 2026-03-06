> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# TOON Format Overview

> Introduction to TOON, a human-readable alternative to JSON

TOON (Tabular Object Oriented Notation) is a human-readable data serialization format designed as an alternative to JSON. It maintains JSON compatibility while offering improved readability, especially for datasets with arrays and tabular structures.

## What is TOON?

TOON is a line-oriented format that uses indentation and special array notations to represent structured data. It's designed to be:

* **Human-readable**: Clean, indented syntax that's easy to scan
* **JSON-compatible**: Every TOON document can be converted to/from JSON
* **Space-efficient**: Tabular arrays reduce repetition compared to JSON
* **Flexible**: Supports multiple delimiters (comma, tab, pipe) for different use cases

## Key Benefits Over JSON

### Reduced Repetition

TOON's tabular array format eliminates repeated key names:

  ```json JSON theme={null}
  [
    {"name": "Alice", "age": 30, "city": "NYC"},
    {"name": "Bob", "age": 25, "city": "LA"},
    {"name": "Carol", "age": 35, "city": "SF"}
  ]
  ```

  ```toon TOON theme={null}
  [3]{name,age,city}:
    Alice,30,NYC
    Bob,25,LA
    Carol,35,SF
  ```

### Better Readability

Indentation-based structure makes hierarchy obvious:

  ```json JSON theme={null}
  {
    "database": {
      "host": "localhost",
      "port": 5432
    }
  }
  ```

  ```toon TOON theme={null}
  database:
    host: localhost
    port: 5432
  ```

### Flexible Array Formats

TOON automatically chooses the best format for each array:

* **Primitive arrays**: Inline comma-separated values
* **Tabular arrays**: Header with field names, rows of values
* **List arrays**: Traditional dash-prefixed list items

## Use Cases

TOON is ideal for:

* **Configuration files**: More readable than JSON, especially with nested structures
* **Data exports**: Tabular format is perfect for database query results
* **API responses**: When human readability matters
* **Test fixtures**: Easier to read and maintain than JSON
* **Log processing**: Line-oriented format is easier to parse and manipulate

## Format Features

  TOON uses 2-space indentation by default and supports three array delimiters: comma (`,`), tab (`\t`), and pipe (`|`).

### Core Elements

* **Objects**: Key-value pairs with colon separators
* **Arrays**: Three specialized formats (primitive, tabular, list)
* **Primitives**: Strings, numbers, booleans, null
* **Quoting**: Smart quoting rules minimize unnecessary quotes

### Optional Features

* **Length markers**: Prefix array lengths with `#` (e.g., `[#3]`)
* **Key folding**: Flatten nested single-key objects (e.g., `user.profile.name`)
* **Path expansion**: Expand dotted keys into nested objects (disabled by default)

## Compatibility

TOON is fully bidirectional with JSON:

```bash  theme={null}
# JSON to TOON
python toon_json_converter.py data.json data.toon

# TOON to JSON
python toon_json_converter.py data.toon data.json

# Batch processing
python toon_json_converter.py data.jsonl output_folder/
python toon_json_converter.py input_folder/ output.jsonl
```

  See the [[Syntax Rules]] and [[Array Formats]] pages for detailed format specifications.

## Quick Example

Here's a complete example showing TOON's features:

  ```json JSON theme={null}
  {
    "users": [
      {"id": 1, "name": "Alice", "active": true},
      {"id": 2, "name": "Bob", "active": false}
    ],
    "config": {
      "timeout": 30,
      "retries": 3
    },
    "tags": ["api", "v2", "stable"]
  }
  ```

  ```toon TOON theme={null}
  users[2]{id,name,active}:
    1,Alice,true
    2,Bob,false
  config:
    timeout: 30
    retries: 3
  tags[3]: api,v2,stable
  ```

## Next Steps

  
    Learn the detailed syntax rules for keys, values, and quoting
  

  
    Understand the three array formats and when to use each
  

  
    See comprehensive real-world examples
  

  
    Get started with the converter tool