---
name: zero-defect-verification
description: Enforces multi-stage code validation (AST -> Ruff -> Mypy -> ASan -> Pytest/GCC) with autonomous self-healing.
---

# Zero-Defect Verification Skill

## Purpose
Ensure no untested, unlinted, or type-unsafe code is delivered.

## Workflow:
1. **Pre-Check**: Run AST syntax check and static analysis (`ruff check`, `mypy`).
2. **Compile-Check (C/C++)**: Use `gcc -std=c11 -O2 -Wall -Wextra -Werror -fsanitize=address,undefined -pthread`.
3. **Dynamic Test**: Run `pytest` or binary test harnesses under AddressSanitizer.
4. **Reflexion Loop**: If any test/lint fails, parse the exact compiler output/stack trace and self-heal before presenting to the user.
