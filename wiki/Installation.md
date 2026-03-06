> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# Installation

> Get started with TOON JSON Converter by downloading the single-file Python script

## Requirements

TOON JSON Converter is a single Python file that requires:

* **Python 3.10+** (uses modern type hints like `list[str]` and pattern matching)
* No external dependencies - uses only Python standard library

## Download

Since TOON JSON Converter is a standalone Python script, installation is simple:

  
    Download `toon_json_converter.py` from the repository and place it in your project directory or a location in your PATH.
  

  
    On Unix-like systems, you can make the script executable:

    ```bash  theme={null}
    chmod +x toon_json_converter.py
    ```
  

  
    Check that Python can run the script:

    ```bash  theme={null}
    python toon_json_converter.py
    ```

    You should see the usage information:

    ```
    Bidirectional TOON ↔ JSON/JSONL Converter

    Usage: python toon_json_converter.py  [output] [options]

    Automatic direction detection:
      .json file      → .toon file
      .jsonl file     → folder of .toon files
      .toon file      → .json file
      folder of .toon → .jsonl file
    ```
  

## Usage as a Module

You can also import and use the converter programmatically in your Python code:

```python  theme={null}
from toon_json_converter import BidirectionalConverter, EncodeOptions, DecodeOptions

# Create a converter instance
converter = BidirectionalConverter()

# Convert files
converter.convert_file("data.json", "data.toon")
```

## Next Steps

  
    Get up and running with your first conversion
  

  
    Learn about encoding and decoding options