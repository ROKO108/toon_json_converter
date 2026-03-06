> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# Options

> Configuration options for encoding and decoding

The TOON JSON Converter provides two configuration classes to control encoding and decoding behavior.

## EncodeOptions

Controls how Python objects are encoded to TOON format.

```python  theme={null}
from toon_json_converter import EncodeOptions, Delimiter

options = EncodeOptions(
    indent_size=2,
    delimiter=Delimiter.COMMA,
    length_marker=False,
    key_folding=False,
    flatten_depth=float('inf')
)
```

### Fields

  Number of spaces per indentation level. Common values are `2` or `4`.

  ```python  theme={null}
  # 2-space indentation (default)
  options = EncodeOptions(indent_size=2)
  # Output:
  # user:
  #   name: Alice

  # 4-space indentation
  options = EncodeOptions(indent_size=4)
  # Output:
  # user:
  #     name: Alice
  ```

  Delimiter used for separating values in primitive and tabular arrays.

  Available values:

  * `Delimiter.COMMA` - Comma delimiter (`,`)
  * `Delimiter.TAB` - Tab delimiter (`\t`)
  * `Delimiter.PIPE` - Pipe delimiter (`|`)

  ```python  theme={null}
  from toon_json_converter import Delimiter

  # Comma (default)
  options = EncodeOptions(delimiter=Delimiter.COMMA)
  # Output: values[3]: 1,2,3

  # Tab
  options = EncodeOptions(delimiter=Delimiter.TAB)
  # Output: values[3 ]: 1\t2\t3

  # Pipe
  options = EncodeOptions(delimiter=Delimiter.PIPE)
  # Output: values[3|]: 1|2|3
  ```

  Whether to add a `#` prefix to array lengths in headers.

  ```python  theme={null}
  # Without length marker (default)
  options = EncodeOptions(length_marker=False)
  # Output: items[5]: 1,2,3,4,5

  # With length marker
  options = EncodeOptions(length_marker=True)
  # Output: items[#5]: 1,2,3,4,5
  ```

  Whether to collapse nested single-key objects using dot notation.

  ```python  theme={null}
  data = {
      "database": {
          "connection": {
              "host": "localhost"
          }
      }
  }

  # Without key folding (default)
  options = EncodeOptions(key_folding=False)
  # Output:
  # database:
  #   connection:
  #     host: localhost

  # With key folding
  options = EncodeOptions(key_folding=True)
  # Output:
  # database.connection.host: localhost
  ```

  Maximum depth for key folding. Controls how many levels deep the key folding will go. Only relevant when `key_folding=True`.

  ```python  theme={null}
  data = {
      "a": {
          "b": {
              "c": {
                  "d": "value"
              }
          }
      }
  }

  # Unlimited depth (default)
  options = EncodeOptions(
      key_folding=True,
      flatten_depth=float('inf')
  )
  # Output: a.b.c.d: value

  # Limited to 2 levels
  options = EncodeOptions(
      key_folding=True,
      flatten_depth=2
  )
  # Output:
  # a.b:
  #   c:
  #     d: value
  ```

### Complete Example

```python  theme={null}
from toon_json_converter import TOONEncoder, EncodeOptions, Delimiter

# Create custom encoding options
options = EncodeOptions(
    indent_size=4,
    delimiter=Delimiter.TAB,
    length_marker=True,
    key_folding=True,
    flatten_depth=2
)

encoder = TOONEncoder(options)

data = {
    "config": {
        "database": {
            "host": "localhost"
        }
    },
    "users": [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
}

toon = encoder.encode(data)
print(toon)
```

Output:

```
config.database.host: localhost
users[#2 ]{name,age}:
    Alice    30
    Bob      25
```

***

## DecodeOptions

Controls how TOON format is decoded to JSON/Python objects.

```python  theme={null}
from toon_json_converter import DecodeOptions

options = DecodeOptions(
    pretty=True,
    indent=2,
    expand_paths=False
)
```

### Fields

  Whether to format JSON output with indentation and newlines. When `False`, produces minified (compact) JSON.

  ```python  theme={null}
  # Pretty formatted JSON (default)
  options = DecodeOptions(pretty=True)
  # Output:
  # {
  #   "name": "Alice",
  #   "age": 30
  # }

  # Compact JSON
  options = DecodeOptions(pretty=False)
  # Output:
  # {"name":"Alice","age":30}
  ```

  Number of spaces per indentation level in JSON output. Only used when `pretty=True`.

  ```python  theme={null}
  # 2-space indentation (default)
  options = DecodeOptions(pretty=True, indent=2)
  # Output:
  # {
  #   "user": {
  #     "name": "Alice"
  #   }
  # }

  # 4-space indentation
  options = DecodeOptions(pretty=True, indent=4)
  # Output:
  # {
  #     "user": {
  #         "name": "Alice"
  #     }
  # }
  ```

  Whether to expand dotted keys (e.g., `database.connection.host`) into nested objects.

  Per TOON specification §13.4, this option is **OFF by default** to preserve dotted keys as literal key names.

  ```python  theme={null}
  # TOON input:
  # database.connection.host: localhost

  # Without path expansion (default)
  options = DecodeOptions(expand_paths=False)
  # Output:
  # {
  #   "database.connection.host": "localhost"
  # }

  # With path expansion
  options = DecodeOptions(expand_paths=True)
  # Output:
  # {
  #   "database": {
  #     "connection": {
  #       "host": "localhost"
  #     }
  #   }
  # }
  ```

### Complete Example

```python  theme={null}
from toon_json_converter import BidirectionalConverter, DecodeOptions

# Create custom decoding options
options = DecodeOptions(
    pretty=True,
    indent=4,
    expand_paths=True
)

converter = BidirectionalConverter(decode_options=options)

# Convert TOON to JSON with custom formatting
converter.convert_file('data.toon', 'data.json')
```

With TOON input:

```
app.name: MyApp
app.version: 1.0.0
server.host: localhost
server.port: 8080
```

JSON output (with `expand_paths=True`):

```json  theme={null}
{
    "app": {
        "name": "MyApp",
        "version": "1.0.0"
    },
    "server": {
        "host": "localhost",
        "port": 8080
    }
}
```

***

## Using Options Together

You can use both encoding and decoding options with the `BidirectionalConverter`:

```python  theme={null}
from toon_json_converter import (
    BidirectionalConverter,
    EncodeOptions,
    DecodeOptions,
    Delimiter
)

converter = BidirectionalConverter(
    encode_options=EncodeOptions(
        indent_size=4,
        delimiter=Delimiter.TAB,
        length_marker=True,
        key_folding=True
    ),
    decode_options=DecodeOptions(
        pretty=True,
        indent=4,
        expand_paths=True
    )
)

# JSON → TOON uses encode_options
converter.convert_file('data.json', 'data.toon')

# TOON → JSON uses decode_options
converter.convert_file('data.toon', 'data.json')
```

## Default Values Summary

### EncodeOptions Defaults

| Field           | Default           | Type        |
| --------------- | ----------------- | ----------- |
| `indent_size`   | `2`               | `int`       |
| `delimiter`     | `Delimiter.COMMA` | `Delimiter` |
| `length_marker` | `False`           | `bool`      |
| `key_folding`   | `False`           | `bool`      |
| `flatten_depth` | `float('inf')`    | `int`       |

### DecodeOptions Defaults

| Field          | Default | Type   |
| -------------- | ------- | ------ |
| `pretty`       | `True`  | `bool` |
| `indent`       | `2`     | `int`  |
| `expand_paths` | `False` | `bool` |