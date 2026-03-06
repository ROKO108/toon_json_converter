> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# Introduction

> Bidirectional command-line tool for converting between TOON and JSON/JSONL formats

# TOON JSON Converter

TOON JSON Converter is a powerful Python-based command-line tool that enables seamless bidirectional conversion between TOON (a human-readable structured data format) and JSON/JSONL formats. With automatic format detection and support for both single-file and batch conversions, it's designed to make data transformation effortless.

## What is TOON?

TOON is a structured data format designed to be more readable and writable than JSON while maintaining full compatibility with JSON's data model. It features:

* **Cleaner syntax** with minimal punctuation
* **Tabular data support** for arrays of objects
* **Flexible delimiters** (comma, tab, pipe)
* **Key folding** for nested structures
* **Human-friendly** with optional line markers

## Key Features

  
    Convert seamlessly between TOON and JSON formats in both directions with automatic format detection
  

  
    Process entire folders of files or convert JSONL files to multiple TOON files in one command
  

  
    Customize output with multiple delimiter options, indentation settings, and formatting preferences
  

  
    Maintains data integrity with proper type handling, escaping, and round-trip conversion support
  

## Conversion Modes

The converter automatically detects the conversion direction based on file extensions:

| Input                   | Output                  | Description                                    |
| ----------------------- | ----------------------- | ---------------------------------------------- |
| `.json` file            | `.toon` file            | Single JSON document to TOON format            |
| `.jsonl` file           | Folder of `.toon` files | Multiple JSON objects to individual TOON files |
| `.toon` file            | `.json` file            | Single TOON document to JSON format            |
| Folder of `.toon` files | `.jsonl` file           | Multiple TOON files to JSON Lines format       |

## Quick Example

Convert a JSON file to TOON format:

```bash  theme={null}
python toon_json_converter.py data.json
```

The tool automatically creates `data.toon` with a human-readable representation:

  ```json data.json theme={null}
  {
    "name": "Alice",
    "age": 30,
    "cities": ["New York", "London", "Tokyo"]
  }
  ```

  ```toon data.toon theme={null}
  name: Alice
  age: 30
  cities[3]: New York, London, Tokyo
  ```

## Use Cases

* **Data interchange** between systems with different format requirements
* **Human-readable data storage** for configuration files and datasets
* **Data transformation pipelines** with support for batch processing
* **API response formatting** to make data more accessible
* **Database exports** to readable tabular formats

## Next Steps

  
    Get started by installing the converter
  

  
    Learn the basics with practical examples
  

  
    Explore all command-line options
  

  
    Understand the TOON format specification