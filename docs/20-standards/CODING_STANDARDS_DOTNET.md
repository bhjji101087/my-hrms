# CODING_STANDARDS_DOTNET.md

# .NET Coding Standards

Target Framework

.NET 10 (current LTS). Pinned via `src/global.json` and `src/Directory.Build.props`
(`net10.0`). NuGet packages are kept at their latest stable versions.

---

# Architecture

Clean Architecture

Domain Driven Design

CQRS where appropriate

Repository Pattern

Unit Of Work

---

# SOLID

Mandatory

---

# Naming Standards

Classes

PascalCase

Methods

PascalCase

Variables

camelCase

Interfaces

Prefix I

Example:

IEmployeeService

---

# API Standards

REST First

Versioned APIs

Swagger Mandatory

---

# Logging

Structured Logging

Correlation Id

Request Tracking

---

# Exception Handling

Global Exception Middleware

No swallowed exceptions

---

# Validation

FluentValidation

---

# Testing

xUnit

Moq

Minimum Coverage

85%

---

# Security

JWT

Role Based Security

Attribute Based Security

Tenant Validation

Every Request

---

# Code Reviews

No direct merge to main branch

PR approval mandatory
