---
name: low-level-systems
description: C11, C++20, and x86_64 systems programming, memory safety, pointer arithmetic, and lock-free concurrency.
---

# Low-Level Systems Skill

## Directives:
- Use explicit memory models (`stdatomic.h`, `memory_order_acquire`, `memory_order_release`).
- Zero memory leaks: verify with AddressSanitizer (`-fsanitize=address`).
- For ring buffers, compute bounds using monotonic modulo or power-of-2 bitmasks `(idx & (cap - 1))` properly.
