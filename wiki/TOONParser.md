> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# TOONParser

> Parse TOON format strings into Python objects

The `TOONParser` class converts TOON format strings into Python data structures (dictionaries, lists, and primitives). It handles indentation parsing, array detection, delimiter recognition, and type conversion.

## Constructor

```python  theme={null}
TOONParser(expand_paths: bool = False)
```

  Whether to expand dotted keys (e.g., `database.connection.host`) into nested objects. When `False`, dotted keys are preserved as literal key names. This matches the `expand_paths` option in [[DecodeOptions]].

### Example

```python  theme={null}
from toon_json_converter import TOONParser

# Standard parser (dotted keys preserved)
parser = TOONParser()

# Parser with path expansion enabled
parser = TOONParser(expand_paths=True)
```

## Methods

### parse

Parse TOON format string into a Python object.

```python  theme={null}
parser.parse(content: str) -> Any
```

  The TOON format string to parse.

  The parsed Python object. Returns:

  * `dict` for TOON objects
  * `list` for TOON arrays
  * Primitives: `str`, `int`, `float`, `bool`, `None`

  Raised if the TOON content is malformed or cannot be parsed.

## Usage Examples

### Basic Object Parsing

```python  theme={null}
from toon_json_converter import TOONParser

parser = TOONParser()

toon_content = """
name: Alice
age: 30
active: true
balance: 1250.5
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'name': 'Alice',
    'age': 30,
    'active': True,
    'balance': 1250.5
}
```

### Nested Objects

```python  theme={null}
toon_content = """
user:
  name: Alice
  email: alice@example.com
status: active
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'user': {
        'name': 'Alice',
        'email': 'alice@example.com'
    },
    'status': 'active'
}
```

### Primitive Arrays

```python  theme={null}
toon_content = """
numbers[5]: 1,2,3,4,5
colors[3]: red,green,blue
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'numbers': [1, 2, 3, 4, 5],
    'colors': ['red', 'green', 'blue']
}
```

### Tabular Arrays

Arrays with field headers are parsed into lists of dictionaries:

```python  theme={null}
toon_content = """
users[3]{name,age,city}:
  Alice,30,NYC
  Bob,25,LA
  Charlie,35,SF
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'users': [
        {'name': 'Alice', 'age': 30, 'city': 'NYC'},
        {'name': 'Bob', 'age': 25, 'city': 'LA'},
        {'name': 'Charlie', 'age': 35, 'city': 'SF'}
    ]
}
```

### List Arrays

```python  theme={null}
toon_content = """
items[3]:
  - type: book
    title: 1984
  - type: movie
    title: Inception
  - simple string
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'items': [
        {'type': 'book', 'title': '1984'},
        {'type': 'movie', 'title': 'Inception'},
        'simple string'
    ]
}
```

### Delimiter Detection

The parser automatically detects delimiters from array headers:

#### Tab Delimiter

```python  theme={null}
toon_content = """
users[2 ]{name,score}:
  Alice\t95
  Bob\t87
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'users': [
        {'name': 'Alice', 'score': 95},
        {'name': 'Bob', 'score': 87}
    ]
}
```

#### Pipe Delimiter

```python  theme={null}
toon_content = "values[3|]: 10|20|30"

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{'values': [10, 20, 30]}
```

### Length Markers

The parser handles length markers (with `#` prefix):

```python  theme={null}
toon_content = "items[#5]: 1,2,3,4,5"

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{'items': [1, 2, 3, 4, 5]}
```

### Path Expansion

When `expand_paths=True`, dotted keys are expanded into nested objects:

```python  theme={null}
parser = TOONParser(expand_paths=True)

toon_content = "database.connection.host: localhost"

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'database': {
        'connection': {
            'host': 'localhost'
        }
    }
}
```

With `expand_paths=False` (default):

```python  theme={null}
parser = TOONParser(expand_paths=False)

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{'database.connection.host': 'localhost'}
```

### Quoted Strings

The parser handles quoted strings and unescapes them:

```python  theme={null}
toon_content = """
simple: hello
with_space: "hello world"
number_like: "123"
reserved: "true"
empty: ""
escaped: "Line 1\\nLine 2"
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'simple': 'hello',
    'with_space': 'hello world',
    'number_like': '123',
    'reserved': 'true',
    'empty': '',
    'escaped': 'Line 1\nLine 2'
}
```

### Special Values

```python  theme={null}
toon_content = """
null_value: null
true_value: true
false_value: false
zero: 0
negative: -42
float: 3.14159
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'null_value': None,
    'true_value': True,
    'false_value': False,
    'zero': 0,
    'negative': -42,
    'float': 3.14159
}
```

### Complex Nested Structure

```python  theme={null}
toon_content = """
project: TOON Converter
version: 1.0.0
contributors[2]{name,role}:
  Alice,Developer
  Bob,Designer
config:
  debug: false
  features[3]: encoding,decoding,validation
"""

data = parser.parse(toon_content)
print(data)
```

Output:

```python  theme={null}
{
    'project': 'TOON Converter',
    'version': '1.0.0',
    'contributors': [
        {'name': 'Alice', 'role': 'Developer'},
        {'name': 'Bob', 'role': 'Designer'}
    ],
    'config': {
        'debug': False,
        'features': ['encoding', 'decoding', 'validation']
    }
}
```

### Reading from Files

```python  theme={null}
from toon_json_converter import TOONParser

parser = TOONParser()

# Read TOON file
with open('data.toon', 'r', encoding='utf-8') as f:
    toon_content = f.read()

data = parser.parse(toon_content)
print(data)
```

### Error Handling

```python  theme={null}
from toon_json_converter import TOONParser

parser = TOONParser()

try:
    data = parser.parse(malformed_content)
except (ValueError, KeyError) as e:
    print(f"Parse error: {e}")
```

## Type Detection

The parser automatically detects and converts types:

| TOON Value       | Python Type | Example                     |
| ---------------- | ----------- | --------------------------- |
| `null`           | `None`      | `value: null` → `None`      |
| `true` / `false` | `bool`      | `active: true` → `True`     |
| Integer          | `int`       | `count: 42` → `42`          |
| Decimal          | `float`     | `price: 19.99` → `19.99`    |
| Quoted string    | `str`       | `name: "Alice"` → `'Alice'` |
| Unquoted string  | `str`       | `name: Alice` → `'Alice'`   |

## Escape Sequences

The parser handles standard escape sequences in quoted strings:

| Escape | Result          |
| ------ | --------------- |
| `\\`   | Backslash       |
| `\"`   | Double quote    |
| `\n`   | Newline         |
| `\r`   | Carriage return |
| `\t`   | Tab             |

```python  theme={null}
toon_content = 'message: "Line 1\\nLine 2\\tTabbed"'
data = parser.parse(toon_content)
print(data['message'])
```

Output:

```
Line 1
Line 2    Tabbed
```

## Configuration

For more control over parsing behavior, use [[DecodeOptions]] with the [[BidirectionalConverter]]:

```python  theme={null}
from toon_json_converter import BidirectionalConverter, DecodeOptions

converter = BidirectionalConverter(
    decode_options=DecodeOptions(
        pretty=True,
        indent=4,
        expand_paths=True
    )
)

converter.convert_file('data.toon', 'data.json')
```