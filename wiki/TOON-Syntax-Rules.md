> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# TOON Syntax Rules

> Detailed syntax rules for the TOON format

TOON uses a clean, indentation-based syntax with smart quoting rules to minimize visual noise.

## Indentation

TOON uses **2-space indentation** by default to represent nesting levels:

```toon  theme={null}
root:
  level1:
    level2: value
```

  Indentation must be consistent throughout the document. Mixing tabs and spaces is not allowed.

## Key-Value Pairs

Keys and values are separated by a colon (`:`) followed by optional whitespace:

```toon  theme={null}
key: value
name: Alice
count: 42
```

### Key Syntax

Keys follow identifier rules and may contain:

* Letters (Unicode): `a-z`, `A-Z`, `α-ω`, etc.
* Digits: `0-9`
* Underscores and dots: `_`, `.`

```toon  theme={null}
userId: 123
first_name: Alice
user.email: alice@example.com
```

### When Keys Need Quotes

Keys must be quoted if they:

* Are empty
* Don't start with a letter or underscore
* Contain special characters (spaces, `:`, `[`, `]`, `{`, `}`, delimiters)

```toon  theme={null}
"user-id": 123
"first name": Alice
"": empty-key
"special:key": value
```

  Keys matching the pattern `^[\w][\w.]*$` don't need quotes (see `toon_json_converter.py:65`).

## Values

### Primitives

TOON supports all JSON primitive types:

#### Null

```toon  theme={null}
missing: null
```

#### Booleans

```toon  theme={null}
active: true
enabled: false
```

#### Numbers

Numbers are written in canonical decimal form (no scientific notation by default):

```toon  theme={null}
count: 42
price: 19.99
negative: -273.15
zero: 0
```

  Leading zeros (e.g., `007`) are treated as strings and must be quoted if intended as strings.

#### Strings

Strings may be unquoted if they follow safe identifier rules:

```toon  theme={null}
name: Alice
status: active
code: ABC123
```

## String Quoting Rules

TOON uses smart quoting to minimize unnecessary quotes. Strings need quotes if they:

### 1. Are Empty or Have Leading/Trailing Whitespace

```toon  theme={null}
empty: ""
spaced: "  value  "
```

### 2. Match Reserved Literals

```toon  theme={null}
value1: "true"    # quoted to avoid boolean interpretation
value2: "false"   # quoted to avoid boolean interpretation
value3: "null"    # quoted to avoid null interpretation
```

### 3. Look Like Numbers

```toon  theme={null}
code: "123"       # quoted to keep as string
phone: "555-0100" # hyphen makes this unambiguous, no quotes needed
padded: "007"     # leading zero requires quotes
```

### 4. Start with a Hyphen

```toon  theme={null}
value: "-special"  # hyphens could be confused with list markers
```

### 5. Contain Special Characters

Quotes are required for strings containing:

* The active delimiter (`,`, `\t`, or `|`)
* Structural characters: `:`, `[`, `]`, `{`, `}`, `"`, `\`
* Newlines, carriage returns, or tabs

```toon  theme={null}
description: "Contains: colon"
csv: "value1,value2,value3"
path: "C:\\Users\\Alice"
```

### 6. Look Like Array or Field Headers

```toon  theme={null}
weird: "[10]"      # quoted to avoid array header interpretation
data: "{a,b,c}"    # quoted to avoid field header interpretation
```

  The quoting rules are implemented in the `QuotingRules` class (`toon_json_converter.py:62-116`).

## Escape Sequences

Inside quoted strings, these escape sequences are supported:

| Escape | Result             |
| ------ | ------------------ |
| `\\`   | Backslash (`\`)    |
| `\"`   | Double quote (`"`) |
| `\n`   | Newline            |
| `\r`   | Carriage return    |
| `\t`   | Tab                |

```toon  theme={null}
message: "Line 1\nLine 2"
path: "C:\\Program Files\\App"
quote: "She said \"hello\""
```

  Unlike JSON, TOON doesn't support `\u` Unicode escapes. Use UTF-8 encoding directly.

## Nested Objects

Objects are represented by indented key-value pairs:

```toon  theme={null}
user:
  name: Alice
  profile:
    age: 30
    city: NYC
```

### Empty Objects

```toon  theme={null}
empty_obj:
default: {}
```

Both represent empty objects in JSON.

## Key Folding (Optional)

When enabled with `--key-folding`, nested single-key objects can be flattened using dot notation:

  ```toon Without Key Folding theme={null}
  user:
    profile:
      settings:
        theme: dark
  ```

  ```toon With Key Folding theme={null}
  user.profile.settings.theme: dark
  ```

  Key folding only works for keys matching `^[A-Za-z_][A-Za-z0-9_]*$` (see `toon_json_converter.py:281`).

## Path Expansion (Optional)

When decoding with `--expand-paths`, dotted keys are expanded into nested objects:

```toon  theme={null}
# In TOON file
user.name: Alice
user.age: 30
```

  ```json Without --expand-paths (default) theme={null}
  {
    "user.name": "Alice",
    "user.age": 30
  }
  ```

  ```json With --expand-paths theme={null}
  {
    "user": {
      "name": "Alice",
      "age": 30
    }
  }
  ```

  Path expansion is **disabled by default** (per §13.4 of the TOON spec). Enable it explicitly with `--expand-paths` if needed.

## Delimiters

TOON supports three delimiters for array values:

### Comma (Default)

```toon  theme={null}
tags[3]: api,v2,stable
```

### Tab

Use `--tab` flag for tab-separated values:

```toon  theme={null}
# Array header: [3 ] (note the space marker)
data[3 ]: value1    value2    value3
```

### Pipe

Use `--pipe` flag for pipe-separated values:

```toon  theme={null}
# Array header: [3|]
data[3|]: value1|value2|value3
```

  Delimiter choice affects when strings need quotes. Choose based on your data content to minimize quoting.

## Comments

  TOON does not currently support comments. Use JSON comments or separate documentation files if needed.

## Complete Example

Here's a complete example demonstrating various syntax rules:

```toon  theme={null}
# User configuration
userId: 12345
first_name: Alice
"user-type": admin
"special:key": "value with: colon"

profile:
  age: 30
  active: true
  score: 98.5
  nickname: null
  bio: "Software engineer\nPython enthusiast"
  
preferences:
  theme: dark
  "font-size": 14
  notifications: false

roles[3]: admin,developer,reviewer
```

  For array syntax rules, see the [[Array Formats]] page.

## Next Steps

  
    Learn about TOON's three array formats
  

  
    See comprehensive real-world examples