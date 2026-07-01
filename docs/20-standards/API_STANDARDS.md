# API_STANDARDS.md

# API Design Standards

---

# API Style

REST First

OpenAPI Required

---

# Versioning

/api/v1

/api/v2

Mandatory.

---

# Naming

Good:

GET /api/v1/employees

Bad:

GET /api/v1/GetEmployees

---

# Response Format

{
"success": true,
"message": "",
"data": {}
}

---

# Error Format

{
"success": false,
"message": "Validation failed",
"errors": []
}

---

# Pagination

Required for list endpoints.

Parameters:

page

pageSize

sort

filter

---

# Filtering

Support:

search

sort

filter

---

# Security

JWT Required

Permission Validation Required

Tenant Validation Required

---

# OpenAPI

Every endpoint documented.

Swagger mandatory.

---

# Logging

CorrelationId

RequestId

Mandatory.

---

# Idempotency

Required for critical operations.
