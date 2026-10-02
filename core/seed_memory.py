#!/usr/bin/env python3
"""
Seed script to initialize ~/.onur_ai/memory.db with default preferences and rules.
This ensures any new machine inherits Onur's exact agent memory settings out of the box.
"""
import sys
from pathlib import Path

# Ensure core directory is in sys.path
core_dir = Path(__file__).resolve().parent
if str(core_dir) not in sys.path:
    sys.path.insert(0, str(core_dir))

from memory import MemoryEngine

DEFAULT_PREFERENCES = [
    ("architecture", "concurrency", "Prefer atomic/lock-free or clear thread-safe semantics", 1.0),
    ("python", "typing", "Always enforce type hints and dataclasses", 1.0),
    ("safety", "risk_gate", "Always ask before modifying public APIs or database schemas", 1.0),
    ("testing", "zero_defect", "Code must pass pytest and ruff before commit", 1.0),
]

def seed_memory():
    engine = MemoryEngine()
    print("🌱 Initializing Long-Term Memory database...")
    for cat, key, val, conf in DEFAULT_PREFERENCES:
        engine.set_preference(cat, key, val, conf)
        print(f"  ✓ [{cat.upper()}] {key} -> {val}")
    print(f"✅ Memory successfully seeded at: {engine.conn}")

if __name__ == "__main__":
    seed_memory()
