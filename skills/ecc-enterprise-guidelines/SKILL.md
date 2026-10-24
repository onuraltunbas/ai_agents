---
name: ecc-enterprise-guidelines
description: Enterprise code standards, clean architecture, resilient APIs, security best practices, and multi-framework guidelines (TypeScript, React, Next.js, Python, FastAPI, Node, Go) from the Elite Coding Companion (ECC). Use when building production-grade enterprise software, designing architecture, or auditing code security.
---

# ECC: Enterprise Coding Companion Guidelines

This skill brings production-tested engineering patterns and enterprise discipline:

## Core Principles
1. **Resilience & Defense-in-Depth**:
   - Explicit input validation and sanitization (Zod, Pydantic, etc.).
   - Granular error handling; never swallow errors silently.
   - Structured logging with correlation IDs and timestamps.
2. **Type Safety & Strict Contracts**:
   - Zero `any` policy in TypeScript; strict mode enabled.
   - Pydantic models for all API request/response payloads in Python.
   - Domain-driven data models with explicit interfaces.
3. **Clean Architecture & Separation of Concerns**:
   - Presentation Layer (Components, Pages, UI)
   - Application Layer (Use Cases, State Management)
   - Domain Layer (Business Rules, Entities)
   - Infrastructure Layer (API Clients, DB Repositories, Websockets)
4. **Security & Authentication**:
   - Cryptographic signatures for sensitive tokens (HMAC, JWT).
   - Rate limiting, CSRF protection, and CORS configuration.
   - OWASP Top 10 mitigation built into every endpoint.
5. **Testing & Observability**:
   - TDD and unit testing for core business rules.
   - Health check endpoints (`/health`, `/ready`).
