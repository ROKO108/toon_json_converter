> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# API Overview

> Programmatic usage of the TOON JSON Converter library

The TOON JSON Converter provides a Python API for programmatic conversion between TOON and JSON formats. This is useful when you need to integrate TOON conversion into your own applications or scripts.

## Installation

The library is a single Python file with no external dependencies beyond Python's standard library:

```python  theme={null}
import toon_json_converter
```

Or import specific classes:

```python  theme={null}
from toon_json_converter import (
    BidirectionalConverter,
    TOONEncoder,
    TOONParser,
    EncodeOptions,
    DecodeOptions,
    Delimiter
)
```

## Quick Start

### Simple Conversion

The easiest way to convert files is using the `BidirectionalConverter` class:

```python  theme={null}
from toon_json_converter import BidirectionalConverter

converter = BidirectionalConverter()

# Automatically detects conversion direction from file extension
converter.convert_file("data.json", "data.toon")  # JSON → TOON
converter.convert_file("data.toon", "data.json")  # TOON → JSON
```

### Encoding JSON to TOON

For direct encoding of Python objects to TOON format:

```python  theme={null}
from toon_json_converter import TOONEncoder

encoder = TOONEncoder()
data = {"name": "Alice", "age": 30, "active": True}
toon_string = encoder.encode(data)
print(toon_string)
```

Output:

```
name: Alice
age: 30
active: true
```

### Decoding TOON to Python

For parsing TOON format into Python objects:

```python  theme={null}
from toon_json_converter import TOONParser

parser = TOONParser()
toon_content = """
name: Alice
age: 30
active: true
"""
data = parser.parse(toon_content)
print(data)
# {'name': 'Alice', 'age': 30, 'active': True}
```

## Core Components

The library provides three main classes:

* **[[BidirectionalConverter]]** - High-level file converter with automatic direction detection
* **[[TOONEncoder]]** - Converts Python objects to TOON format strings
* **[[TOONParser]]** - Parses TOON format strings into Python objects

And two configuration classes:

* **[[EncodeOptions]]** - Controls JSON → TOON encoding behavior
* **[[DecodeOptions]]** - Controls TOON → JSON decoding behavior

## Working with Options

```python  theme={null}
from toon_json_converter import (
    BidirectionalConverter,
    EncodeOptions,
    DecodeOptions,
    Delimiter
)

# Configure encoding options
encode_opts = EncodeOptions(
    indent_size=4,
    delimiter=Delimiter.TAB,
    length_marker=True,
    key_folding=True
)

# Configure decoding options
decode_opts = DecodeOptions(
    pretty=True,
    indent=4,
    expand_paths=True
)

# Create converter with custom options
converter = BidirectionalConverter(
    encode_options=encode_opts,
    decode_options=decode_opts
)

converter.convert_file("input.json", "output.toon")
```

## Next Steps

* Learn about the [[BidirectionalConverter]] for file-based conversions
* Use [[TOONEncoder]] for direct object encoding
* Use [[TOONParser]] for parsing TOON strings
* Configure behavior with [[Options]]