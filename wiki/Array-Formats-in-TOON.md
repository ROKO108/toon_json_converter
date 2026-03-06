> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# Array Formats in TOON

> Understanding TOON's three array formats - primitive, tabular, and list arrays

TOON provides three specialized array formats, each optimized for different data structures. The converter automatically selects the best format based on array contents.

## Array Format Selection

The `ArrayClassifier` class (`toon_json_converter.py:195-223`) determines which format to use:

1. **Primitive Array**: All elements are primitives (not objects or arrays)
2. **Tabular Array**: All elements are objects with identical keys and primitive values
3. **List Array**: Everything else (mixed types, nested structures, non-uniform objects)

## Primitive Arrays

Primitive arrays contain only strings, numbers, booleans, and null values.

### Syntax

```
[length]: value1,value2,value3
```

* `length`: Number of elements in the array
* Values are separated by the active delimiter (comma by default)
* Values appear on the same line as the header

### Examples

```toon  theme={null}
tags[3]: api,v2,stable
numbers[5]: 1,2,3,4,5
flags[3]: true,false,true
mixed[4]: 42,hello,true,null
```

  ```toon TOON theme={null}
  colors[4]: red,green,blue,yellow
  scores[3]: 95,87,92
  ```

  ```json JSON theme={null}
  {
    "colors": ["red", "green", "blue", "yellow"],
    "scores": [95, 87, 92]
  }
  ```

### Quoting in Primitive Arrays

Strings follow the same quoting rules as regular values:

```toon  theme={null}
names[3]: Alice,Bob,"O'Connor"
special[3]: "value,with,commas",normal,"has: colon"
```

  Empty arrays are valid: `empty[0]:`

## Tabular Arrays

Tabular arrays are perfect for arrays of uniform objects - like database query results or CSV data.

### Syntax

```
[length][delimiter]{field1,field2,field3}:
  value1,value2,value3
  value1,value2,value3
```

* `length`: Number of rows
* `delimiter`: Optional marker (space for tab, `|` for pipe, omitted for comma)
* `{field1,field2,...}`: Field names (always comma-separated, per §9/§11)
* Each row contains values in the same order as fields

### Basic Example

  ```toon TOON theme={null}
  users[3]{id,name,age}:
    1,Alice,30
    2,Bob,25
    3,Carol,35
  ```

  ```json JSON theme={null}
  {
    "users": [
      {"id": 1, "name": "Alice", "age": 30},
      {"id": 2, "name": "Bob", "age": 25},
      {"id": 3, "name": "Carol", "age": 35}
    ]
  }
  ```

### Benefits

Compare the space savings:

  ```json JSON (211 characters) theme={null}
  [
    {"name": "Alice", "score": 95, "passed": true},
    {"name": "Bob", "score": 87, "passed": true},
    {"name": "Carol", "score": 72, "passed": true},
    {"name": "Dave", "score": 64, "passed": false}
  ]
  ```

  ```toon TOON (121 characters) theme={null}
  [4]{name,score,passed}:
    Alice,95,true
    Bob,87,true
    Carol,72,true
    Dave,64,false
  ```

**\~43% space reduction** while maintaining readability!

### Requirements for Tabular Format

Tabular format is only used when:

1. Array is non-empty
2. All elements are objects
3. All objects have the **exact same keys**
4. All values are **primitives** (no nested objects/arrays)

```toon  theme={null}
# Valid - uniform structure
products[2]{id,name,price}:
  1,Widget,9.99
  2,Gadget,19.99

# Invalid - mixed keys (becomes list array instead)
data[2]:
  - id: 1
    name: Alice
  - id: 2
    email: bob@example.com

# Invalid - nested object (becomes list array instead)
users[2]:
  - id: 1
    profile:
      name: Alice
```

### Delimiter Variants

#### Comma (Default)

```toon  theme={null}
data[2]{a,b,c}:
  1,2,3
  4,5,6
```

#### Tab (`--tab` flag)

```toon  theme={null}
# Note the space marker after length
data[2 ]{a,b,c}:
  1    2    3
  4    5    6
```

  The space marker `[2 ]` indicates tab delimiter. Field names in `{a,b,c}` are always comma-separated.

#### Pipe (`--pipe` flag)

```toon  theme={null}
# Note the pipe marker after length
data[2|]{a,b,c}:
  1|2|3
  4|5|6
```

### Complex Tabular Example

  ```toon TOON theme={null}
  orders[3]{orderId,customer,amount,status}:
    1001,"Smith, John",150.00,shipped
    1002,Alice,75.50,pending
    1003,"O'Brien",200.00,delivered
  ```

  ```json JSON theme={null}
  {
    "orders": [
      {
        "orderId": 1001,
        "customer": "Smith, John",
        "amount": 150.00,
        "status": "shipped"
      },
      {
        "orderId": 1002,
        "customer": "Alice",
        "amount": 75.50,
        "status": "pending"
      },
      {
        "orderId": 1003,
        "customer": "O'Brien",
        "amount": 200.00,
        "status": "delivered"
      }
    ]
  }
  ```

## List Arrays

List arrays handle everything else: mixed types, nested structures, and non-uniform objects.

### Syntax

```
[length]:
  - item1
  - item2
  - item3
```

* Each item is prefixed with `- ` (dash-space)
* Items are indented one level from the header
* Items can be primitives, objects, or arrays

### Simple List

  ```toon TOON theme={null}
  colors[3]:
    - red
    - green
    - blue
  ```

  ```json JSON theme={null}
  {
    "colors": ["red", "green", "blue"]
  }
  ```

  This becomes a list array instead of a primitive array only when manually specified. The converter automatically uses primitive format for simple values.

### List of Objects

  ```toon TOON theme={null}
  users[2]:
    - id: 1
      name: Alice
      active: true
    - id: 2
      name: Bob
      active: false
  ```

  ```json JSON theme={null}
  {
    "users": [
      {"id": 1, "name": "Alice", "active": true},
      {"id": 2, "name": "Bob", "active": false}
    ]
  }
  ```

### Mixed Types

```toon  theme={null}
mixed[4]:
  - 42
  - hello
  - true
  - name: Alice
    age: 30
```

### Nested Arrays

```toon  theme={null}
matrix[3]:
  - [3]: 1,2,3
  - [3]: 4,5,6
  - [3]: 7,8,9
```

### Complex Nested Example

  ```toon TOON theme={null}
  teams[2]:
    - name: Engineering
      members[3]{id,name,role}:
        1,Alice,lead
        2,Bob,dev
        3,Carol,dev
      active: true
    - name: Marketing
      members[2]{id,name,role}:
        4,Dave,manager
        5,Eve,analyst
      active: true
  ```

  ```json JSON theme={null}
  {
    "teams": [
      {
        "name": "Engineering",
        "members": [
          {"id": 1, "name": "Alice", "role": "lead"},
          {"id": 2, "name": "Bob", "role": "dev"},
          {"id": 3, "name": "Carol", "role": "dev"}
        ],
        "active": true
      },
      {
        "name": "Marketing",
        "members": [
          {"id": 4, "name": "Dave", "role": "manager"},
          {"id": 5, "name": "Eve", "role": "analyst"}
        ],
        "active": true
      }
    ]
  }
  ```

## Array Headers in Different Contexts

### Top-Level Array

```toon  theme={null}
[3]: red,green,blue
```

No key is needed for top-level arrays.

### Named Array in Object

```toon  theme={null}
colors[3]: red,green,blue
```

### Nested Array in List Item

First entry shares the dash line:

```toon  theme={null}
data[2]:
  - tags[3]: a,b,c
    count: 10
  - tags[2]: x,y
    count: 5
```

## Optional: Length Markers

Use `--length-marker` flag to add `#` prefix to array lengths:

  ```toon Without --length-marker theme={null}
  data[100]: ...
  ```

  ```toon With --length-marker theme={null}
  data[#100]: ...
  ```

  Length markers make array sizes more visually distinct, useful for datasets with many arrays.

## Field Notation

Field lists in tabular arrays always use comma separators, regardless of the delimiter used for values:

```toon  theme={null}
# Comma delimiter - fields and values both use commas
data[2]{a,b,c}:
  1,2,3

# Tab delimiter - fields use commas, values use tabs
data[2 ]{a,b,c}:
  1    2    3

# Pipe delimiter - fields use commas, values use pipes
data[2|]{a,b,c}:
  1|2|3
```

  This is per §9/§11 of the TOON spec (see `toon_json_converter.py:252-253`).

## Empty Arrays

All formats support empty arrays:

```toon  theme={null}
empty_primitive[0]:
empty_list[0]:
empty_tabular[0]{a,b,c}:
```

## Performance Considerations

### Space Efficiency

* **Primitive arrays**: Most compact for simple lists
* **Tabular arrays**: Excellent for uniform objects (40-60% space savings vs JSON)
* **List arrays**: Similar to JSON but with cleaner formatting

### Parsing Speed

* **Primitive arrays**: Fastest to parse (single line)
* **Tabular arrays**: Fast (no repeated key parsing)
* **List arrays**: Standard parsing speed

## Next Steps

  
    See comprehensive real-world examples
  

  
    Learn about delimiter and format options