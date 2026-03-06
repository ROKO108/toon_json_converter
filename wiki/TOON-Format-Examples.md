> ## Documentation Index
> Fetch the complete documentation index at: llms.txt
> Use this file to discover all available pages before exploring further.

# TOON Format Examples

> Comprehensive real-world examples demonstrating TOON's capabilities

This page provides practical examples showing how TOON handles common data structures and real-world scenarios.

## Basic Examples

### Simple Configuration

  ```toon TOON theme={null}
  appName: MyApp
  version: 1.2.3
  environment: production

  server:
    host: localhost
    port: 8080
    ssl: true

  features:
    auth: true
    analytics: false
    beta: false
  ```

  ```json JSON theme={null}
  {
    "appName": "MyApp",
    "version": "1.2.3",
    "environment": "production",
    "server": {
      "host": "localhost",
      "port": 8080,
      "ssl": true
    },
    "features": {
      "auth": true,
      "analytics": false,
      "beta": false
    }
  }
  ```

### User Profile

  ```toon TOON theme={null}
  userId: 12345
  username: alice_dev
  email: alice@example.com
  verified: true
  createdAt: 2024-01-15T10:30:00Z

  profile:
    firstName: Alice
    lastName: Johnson
    bio: "Software engineer\nPython enthusiast"
    location: San Francisco, CA
    
  settings:
    theme: dark
    notifications: true
    language: en-US

  roles[3]: developer,admin,reviewer
  ```

  ```json JSON theme={null}
  {
    "userId": 12345,
    "username": "alice_dev",
    "email": "alice@example.com",
    "verified": true,
    "createdAt": "2024-01-15T10:30:00Z",
    "profile": {
      "firstName": "Alice",
      "lastName": "Johnson",
      "bio": "Software engineer\nPython enthusiast",
      "location": "San Francisco, CA"
    },
    "settings": {
      "theme": "dark",
      "notifications": true,
      "language": "en-US"
    },
    "roles": ["developer", "admin", "reviewer"]
  }
  ```

## Tabular Data Examples

### Database Query Results

TOON excels at representing tabular data:

  ```toon TOON theme={null}
  users[5]{id,username,email,lastLogin,active}:
    1,alice,alice@example.com,2024-03-15T10:30:00Z,true
    2,bob,bob@example.com,2024-03-14T15:45:00Z,true
    3,carol,carol@example.com,2024-03-10T08:20:00Z,false
    4,dave,dave@example.com,2024-03-16T09:15:00Z,true
    5,eve,eve@example.com,2024-03-13T14:30:00Z,true
  ```

  ```json JSON theme={null}
  {
    "users": [
      {"id": 1, "username": "alice", "email": "alice@example.com", "lastLogin": "2024-03-15T10:30:00Z", "active": true},
      {"id": 2, "username": "bob", "email": "bob@example.com", "lastLogin": "2024-03-14T15:45:00Z", "active": true},
      {"id": 3, "username": "carol", "email": "carol@example.com", "lastLogin": "2024-03-10T08:20:00Z", "active": false},
      {"id": 4, "username": "dave", "email": "dave@example.com", "lastLogin": "2024-03-16T09:15:00Z", "active": true},
      {"id": 5, "username": "eve", "email": "eve@example.com", "lastLogin": "2024-03-13T14:30:00Z", "active": true}
    ]
  }
  ```

**Space comparison**: TOON is \~45% smaller for this dataset.

### Sales Data

  ```toon TOON theme={null}
  quarterly_sales[4]{quarter,revenue,costs,profit,growth}:
    Q1-2024,1250000,850000,400000,12.5
    Q2-2024,1420000,920000,500000,15.3
    Q3-2024,1680000,980000,700000,18.2
    Q4-2024,1890000,1050000,840000,22.1

  total_revenue: 6240000
  total_profit: 2440000
  ```

  ```json JSON theme={null}
  {
    "quarterly_sales": [
      {"quarter": "Q1-2024", "revenue": 1250000, "costs": 850000, "profit": 400000, "growth": 12.5},
      {"quarter": "Q2-2024", "revenue": 1420000, "costs": 920000, "profit": 500000, "growth": 15.3},
      {"quarter": "Q3-2024", "revenue": 1680000, "costs": 980000, "profit": 700000, "growth": 18.2},
      {"quarter": "Q4-2024", "revenue": 1890000, "costs": 1050000, "profit": 840000, "growth": 22.1}
    ],
    "total_revenue": 6240000,
    "total_profit": 2440000
  }
  ```

### Product Catalog

  ```toon TOON theme={null}
  products[4]{sku,name,price,stock,category}:
    WDG-001,Widget Pro,29.99,150,widgets
    GDG-002,Gadget Plus,49.99,87,gadgets
    WDG-003,Widget Lite,19.99,203,widgets
    ACC-004,"Universal Adapter, 5V",12.99,324,accessories
  ```

  ```json JSON theme={null}
  {
    "products": [
      {"sku": "WDG-001", "name": "Widget Pro", "price": 29.99, "stock": 150, "category": "widgets"},
      {"sku": "GDG-002", "name": "Gadget Plus", "price": 49.99, "stock": 87, "category": "gadgets"},
      {"sku": "WDG-003", "name": "Widget Lite", "price": 19.99, "stock": 203, "category": "widgets"},
      {"sku": "ACC-004", "name": "Universal Adapter, 5V", "price": 12.99, "stock": 324, "category": "accessories"}
    ]
  }
  ```

  Notice how the comma in "Universal Adapter, 5V" is automatically quoted to avoid delimiter confusion.

## Nested Structures

### API Response

  ```toon TOON theme={null}
  status: success
  timestamp: 2024-03-15T10:30:00Z

  data:
    users[3]{id,name,role}:
      1,Alice,admin
      2,Bob,user
      3,Carol,moderator
    
    pagination:
      page: 1
      per_page: 10
      total: 3
      total_pages: 1

  meta:
    request_id: req_abc123xyz
    duration_ms: 45
  ```

  ```json JSON theme={null}
  {
    "status": "success",
    "timestamp": "2024-03-15T10:30:00Z",
    "data": {
      "users": [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"},
        {"id": 3, "name": "Carol", "role": "moderator"}
      ],
      "pagination": {
        "page": 1,
        "per_page": 10,
        "total": 3,
        "total_pages": 1
      }
    },
    "meta": {
      "request_id": "req_abc123xyz",
      "duration_ms": 45
    }
  }
  ```

### Organization Hierarchy

  ```toon TOON theme={null}
  organization:
    name: TechCorp
    founded: 2015
    
    departments[3]:
      - name: Engineering
        headCount: 45
        teams[2]{name,size,lead}:
          Backend,12,Alice
          Frontend,8,Bob
      
      - name: Product
        headCount: 15
        teams[2]{name,size,lead}:
          Design,5,Carol
          Research,3,Dave
      
      - name: Sales
        headCount: 20
        regions[3]: NA,EMEA,APAC
  ```

  ```json JSON theme={null}
  {
    "organization": {
      "name": "TechCorp",
      "founded": 2015,
      "departments": [
        {
          "name": "Engineering",
          "headCount": 45,
          "teams": [
            {"name": "Backend", "size": 12, "lead": "Alice"},
            {"name": "Frontend", "size": 8, "lead": "Bob"}
          ]
        },
        {
          "name": "Product",
          "headCount": 15,
          "teams": [
            {"name": "Design", "size": 5, "lead": "Carol"},
            {"name": "Research", "size": 3, "lead": "Dave"}
          ]
        },
        {
          "name": "Sales",
          "headCount": 20,
          "regions": ["NA", "EMEA", "APAC"]
        }
      ]
    }
  }
  ```

## Complex Real-World Examples

### Test Suite Configuration

  ```toon TOON theme={null}
  testSuite: API Integration Tests
  version: 2.1.0
  timeout: 30000
  retries: 3

  envs[3]{name,baseURL,apiKey}:
    dev,https://dev.api.example.com,dev_key_123
    staging,https://staging.api.example.com,stg_key_456
    prod,https://api.example.com,prod_key_789

  tests[4]:
    - name: User Authentication
      endpoint: /auth/login
      method: POST
      expectedStatus: 200
      assertions[3]:
        - field: token
          type: string
        - field: expiresIn
          type: number
        - field: user.id
          type: number
    
    - name: Create User
      endpoint: /users
      method: POST
      expectedStatus: 201
      headers[2]{key,value}:
        Content-Type,application/json
        Authorization,Bearer {{token}}
      body:
        username: testuser
        email: test@example.com
    
    - name: Get User List
      endpoint: /users
      method: GET
      expectedStatus: 200
      params[2]{key,value}:
        page,1
        limit,10
    
    - name: Delete User
      endpoint: /users/{{userId}}
      method: DELETE
      expectedStatus: 204
  ```

  ```json JSON theme={null}
  {
    "testSuite": "API Integration Tests",
    "version": "2.1.0",
    "timeout": 30000,
    "retries": 3,
    "envs": [
      {"name": "dev", "baseURL": "https://dev.api.example.com", "apiKey": "dev_key_123"},
      {"name": "staging", "baseURL": "https://staging.api.example.com", "apiKey": "stg_key_456"},
      {"name": "prod", "baseURL": "https://api.example.com", "apiKey": "prod_key_789"}
    ],
    "tests": [
      {
        "name": "User Authentication",
        "endpoint": "/auth/login",
        "method": "POST",
        "expectedStatus": 200,
        "assertions": [
          {"field": "token", "type": "string"},
          {"field": "expiresIn", "type": "number"},
          {"field": "user.id", "type": "number"}
        ]
      },
      {
        "name": "Create User",
        "endpoint": "/users",
        "method": "POST",
        "expectedStatus": 201,
        "headers": [
          {"key": "Content-Type", "value": "application/json"},
          {"key": "Authorization", "value": "Bearer {{token}}"}
        ],
        "body": {
          "username": "testuser",
          "email": "test@example.com"
        }
      },
      {
        "name": "Get User List",
        "endpoint": "/users",
        "method": "GET",
        "expectedStatus": 200,
        "params": [
          {"key": "page", "value": 1},
          {"key": "limit", "value": 10}
        ]
      },
      {
        "name": "Delete User",
        "endpoint": "/users/{{userId}}",
        "method": "DELETE",
        "expectedStatus": 204
      }
    ]
  }
  ```

### Machine Learning Dataset

  ```toon TOON theme={null}
  dataset: Customer Churn Prediction
  version: 1.0.0
  samples: 5000

  features[8]{name,type,min,max,mean,stddev}:
    age,numeric,18,95,42.5,15.2
    tenure_months,numeric,1,120,34.8,22.1
    monthly_charges,numeric,18.25,118.75,64.76,30.09
    total_charges,numeric,18.80,8684.80,2283.30,2266.77
    contract_type,categorical,0,2,1.0,0.82
    payment_method,categorical,0,3,1.5,1.12
    internet_service,categorical,0,2,1.2,0.75
    num_services,numeric,0,6,2.8,1.5

  target:
    name: churn
    type: binary
    distribution[2]{label,count,percentage}:
      0,3652,73.04
      1,1348,26.96

  splits[3]{name,samples,percentage}:
    train,3500,70.0
    validation,750,15.0
    test,750,15.0
  ```

  ```json JSON theme={null}
  {
    "dataset": "Customer Churn Prediction",
    "version": "1.0.0",
    "samples": 5000,
    "features": [
      {"name": "age", "type": "numeric", "min": 18, "max": 95, "mean": 42.5, "stddev": 15.2},
      {"name": "tenure_months", "type": "numeric", "min": 1, "max": 120, "mean": 34.8, "stddev": 22.1},
      {"name": "monthly_charges", "type": "numeric", "min": 18.25, "max": 118.75, "mean": 64.76, "stddev": 30.09},
      {"name": "total_charges", "type": "numeric", "min": 18.80, "max": 8684.80, "mean": 2283.30, "stddev": 2266.77},
      {"name": "contract_type", "type": "categorical", "min": 0, "max": 2, "mean": 1.0, "stddev": 0.82},
      {"name": "payment_method", "type": "categorical", "min": 0, "max": 3, "mean": 1.5, "stddev": 1.12},
      {"name": "internet_service", "type": "categorical", "min": 0, "max": 2, "mean": 1.2, "stddev": 0.75},
      {"name": "num_services", "type": "numeric", "min": 0, "max": 6, "mean": 2.8, "stddev": 1.5}
    ],
    "target": {
      "name": "churn",
      "type": "binary",
      "distribution": [
        {"label": 0, "count": 3652, "percentage": 73.04},
        {"label": 1, "count": 1348, "percentage": 26.96}
      ]
    },
    "splits": [
      {"name": "train", "samples": 3500, "percentage": 70.0},
      {"name": "validation", "samples": 750, "percentage": 15.0},
      {"name": "test", "samples": 750, "percentage": 15.0}
    ]
  }
  ```

## Delimiter Variants

### Tab-Separated Values

Use `--tab` flag for tab-separated data:

```toon  theme={null}
# Array header shows space marker: [3 ]
data[3 ]{name    age    city}:
  Alice    30    NYC
  Bob    25    LA
  Carol    35    SF
```

  Tab delimiters are ideal for data with many commas or when importing from TSV files.

### Pipe-Separated Values

Use `--pipe` flag for pipe-separated data:

```toon  theme={null}
# Array header shows pipe marker: [3|]
data[3|]{name,age,city}:
  Alice|30|NYC
  Bob|25|LA
  Carol|35|SF
```

  Pipe delimiters work well when your data contains both commas and tabs.

## Edge Cases

### Special Characters in Data

  ```toon TOON theme={null}
  data[4]{field,value}:
    "with,comma","Contains, commas"
    "with:colon","Key: value format"
    "with\"quote","She said \"hello\""
    "with\nline","Line 1\nLine 2"
  ```

  ```json JSON theme={null}
  {
    "data": [
      {"field": "with,comma", "value": "Contains, commas"},
      {"field": "with:colon", "value": "Key: value format"},
      {"field": "with\"quote", "value": "She said \"hello\""},
      {"field": "with\nline", "value": "Line 1\nLine 2"}
    ]
  }
  ```

### Empty and Null Values

  ```toon TOON theme={null}
  data[5]{id,name,email,phone}:
    1,Alice,alice@example.com,555-0100
    2,Bob,null,555-0101
    3,Carol,carol@example.com,null
    4,"","",""
    5,Eve,eve@example.com,555-0103
  ```

  ```json JSON theme={null}
  {
    "data": [
      {"id": 1, "name": "Alice", "email": "alice@example.com", "phone": "555-0100"},
      {"id": 2, "name": "Bob", "email": null, "phone": "555-0101"},
      {"id": 3, "name": "Carol", "email": "carol@example.com", "phone": null},
      {"id": 4, "name": "", "email": "", "phone": ""},
      {"id": 5, "name": "Eve", "email": "eve@example.com", "phone": "555-0103"}
    ]
  }
  ```

### Mixed Primitives

  ```toon TOON theme={null}
  mixed[8]: 42,hello,true,null,3.14,false,"quoted string",0
  ```

  ```json JSON theme={null}
  {
    "mixed": [42, "hello", true, null, 3.14, false, "quoted string", 0]
  }
  ```

## Optional Features

### Length Markers

Use `--length-marker` for explicit array size indicators:

  ```toon Without --length-marker theme={null}
  data[100]{id,value}:
    ...
  ```

  ```toon With --length-marker theme={null}
  data[#100]{id,value}:
    ...
  ```

### Key Folding

Use `--key-folding` to flatten nested single-key objects:

  ```toon Without --key-folding theme={null}
  user:
    profile:
      settings:
        theme: dark
  ```

  ```toon With --key-folding theme={null}
  user.profile.settings.theme: dark
  ```

  Both represent the same nested structure in JSON.

## Performance Comparison

Space savings on a real-world 1000-record dataset:

| Format            | Size   | Savings  |
| ----------------- | ------ | -------- |
| JSON              | 145 KB | baseline |
| JSON (minified)   | 89 KB  | 39%      |
| TOON (tabular)    | 52 KB  | 64%      |
| TOON (compressed) | 12 KB  | 92%      |

  TOON's tabular format provides significant space savings while maintaining readability, making it ideal for version control and human review.

## Next Steps

  
    Learn how to convert files with the CLI tool
  

  
    Explore all available conversion options
  

  
    Use TOON in your Python applications
  

  
    Return to the format overview