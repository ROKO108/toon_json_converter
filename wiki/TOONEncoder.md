> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# TOONEncoder

> Encode Python objects to TOON format strings

The `TOONEncoder` class converts Python data structures (dictionaries, lists, primitives) into TOON format strings. It handles proper indentation, quoting, delimiter formatting, and array detection.

## Constructor

```python  theme={null}
TOONEncoder(options: EncodeOptions | None = None)
```

  Configuration options for encoding. If not provided, uses default [[EncodeOptions]].

### Example

```python  theme={null}
from toon_json_converter import TOONEncoder, EncodeOptions, Delimiter

# Create encoder with custom options
encoder = TOONEncoder(
    options=EncodeOptions(
        indent_size=4,
        delimiter=Delimiter.TAB,
        length_marker=True,
        key_folding=True
    )
)
```

## Methods

### encode

Convert a Python object to TOON format string.

```python  theme={null}
encoder.encode(data: Any) -> str
```

  The Python object to encode. Supports:

  * Dictionaries (converted to TOON objects)
  * Lists (converted to TOON arrays)
  * Primitives: `str`, `int`, `float`, `bool`, `None`
  * Nested structures of the above types

  The TOON format string representation of the input data.

## Usage Examples

### Basic Object Encoding

```python  theme={null}
from toon_json_converter import TOONEncoder

encoder = TOONEncoder()

data = {
    "name": "Alice",
    "age": 30,
    "active": True,
    "balance": 1250.50
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
name: Alice
age: 30
active: true
balance: 1250.5
```

### Nested Objects

```python  theme={null}
data = {
    "user": {
        "name": "Alice",
        "email": "alice@example.com"
    },
    "status": "active"
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
user:
  name: Alice
  email: alice@example.com
status: active
```

### Primitive Arrays

Arrays containing only primitive values (no objects or nested arrays) are formatted inline:

```python  theme={null}
data = {
    "numbers": [1, 2, 3, 4, 5],
    "colors": ["red", "green", "blue"]
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
numbers[5]: 1,2,3,4,5
colors[3]: red,green,blue
```

### Tabular Arrays

Arrays of objects with identical keys are formatted as tables:

```python  theme={null}
data = {
    "users": [
        {"name": "Alice", "age": 30, "city": "NYC"},
        {"name": "Bob", "age": 25, "city": "LA"},
        {"name": "Charlie", "age": 35, "city": "SF"}
    ]
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
users[3]{name,age,city}:
  Alice,30,NYC
  Bob,25,LA
  Charlie,35,SF
```

### List Arrays

Arrays with mixed or complex items use dash notation:

```python  theme={null}
data = {
    "items": [
        {"type": "book", "title": "1984"},
        {"type": "movie", "title": "Inception"},
        "simple string"
    ]
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
items[3]:
  - type: book
    title: 1984
  - type: movie
    title: Inception
  - simple string
```

### Custom Delimiters

#### Tab Delimiter

```python  theme={null}
from toon_json_converter import TOONEncoder, EncodeOptions, Delimiter

encoder = TOONEncoder(
    options=EncodeOptions(delimiter=Delimiter.TAB)
)

data = {
    "users": [
        {"name": "Alice", "score": 95},
        {"name": "Bob", "score": 87}
    ]
}

toon = encoder.encode(data)
print(toon)
```

Output (tabs shown as multiple spaces):

```
users[2 ]{name,score}:
  Alice    95
  Bob      87
```

#### Pipe Delimiter

```python  theme={null}
encoder = TOONEncoder(
    options=EncodeOptions(delimiter=Delimiter.PIPE)
)

data = {"values": [10, 20, 30]}
toon = encoder.encode(data)
print(toon)
```

Output:

```
values[3|]: 10|20|30
```

### Length Markers

Add `#` prefix to array lengths for clarity:

```python  theme={null}
encoder = TOONEncoder(
    options=EncodeOptions(length_marker=True)
)

data = {
    "items": [1, 2, 3, 4, 5]
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
items[#5]: 1,2,3,4,5
```

### Key Folding

Collapse nested single-key objects using dot notation:

```python  theme={null}
encoder = TOONEncoder(
    options=EncodeOptions(key_folding=True)
)

data = {
    "database": {
        "connection": {
            "host": "localhost"
        }
    }
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
database.connection.host: localhost
```

Without key folding:

```
database:
  connection:
    host: localhost
```

### String Quoting

Strings are automatically quoted when necessary:

```python  theme={null}
data = {
    "simple": "hello",           # No quotes needed
    "with_space": "hello world", # Quotes needed
    "number_like": "123",        # Quotes needed
    "reserved": "true",          # Quotes needed
    "empty": ""                  # Quotes needed
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
simple: hello
with_space: "hello world"
number_like: "123"
reserved: "true"
empty: ""
```

### Special Values

```python  theme={null}
data = {
    "null_value": None,
    "true_value": True,
    "false_value": False,
    "zero": 0,
    "negative": -42,
    "float": 3.14159
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
null_value: null
true_value: true
false_value: false
zero: 0
negative: -42
float: 3.14159
```

### Complex Nested Structure

```python  theme={null}
data = {
    "project": "TOON Converter",
    "version": "1.0.0",
    "contributors": [
        {"name": "Alice", "role": "Developer"},
        {"name": "Bob", "role": "Designer"}
    ],
    "config": {
        "debug": False,
        "features": ["encoding", "decoding", "validation"]
    }
}

encoder = TOONEncoder()
toon = encoder.encode(data)
print(toon)
```

Output:

```
project: TOON Converter
version: 1.0.0
contributors[2]{name,role}:
  Alice,Developer
  Bob,Designer
config:
  debug: false
  features[3]: encoding,decoding,validation
```

## Type Normalization

The encoder automatically normalizes Python types to JSON-compatible values:

* `float('nan')` and `float('inf')` → `null`
* `-0.0` → `0`
* Non-primitive objects → converted to strings with `str()`
* Tuples → converted to lists

```python  theme={null}
import math

data = {
    "infinity": math.inf,
    "not_a_number": math.nan,
    "negative_zero": -0.0
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
infinity: null
not_a_number: null
negative_zero: 0
```

## Configuration

For detailed information on encoding options, see [[EncodeOptions]].