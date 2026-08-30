import sqlite3
import os
import json
import time
from typing import List, Dict, Any, Optional

DB_PATH = "/home/onur/.onur_ai/memory.db"

class MemoryEngine:
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                key TEXT UNIQUE,
                value TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project TEXT,
                decision_summary TEXT,
                rationale TEXT,
                approved_by_user INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS project_profiles (
                repo_path TEXT PRIMARY KEY,
                project_type TEXT,
                test_command TEXT,
                build_command TEXT,
                notes TEXT
            )
            """)

    def set_preference(self, category: str, key: str, value: str, confidence: float = 1.0):
        with self.conn:
            self.conn.execute("""
            INSERT INTO preferences (category, key, value, confidence)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                confidence = excluded.confidence
            """, (category, key, value, confidence))

    def get_all_preferences(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, key, value FROM preferences ORDER BY category")
        rows = cursor.fetchall()
        return [{"category": r[0], "key": r[1], "value": r[2]} for r in rows]

    def record_decision(self, project: str, summary: str, rationale: str, approved: bool):
        with self.conn:
            self.conn.execute("""
            INSERT INTO decisions (project, decision_summary, rationale, approved_by_user)
            VALUES (?, ?, ?, ?)
            """, (project, summary, rationale, 1 if approved else 0))

    def get_context_prompt_fragment(self) -> str:
        prefs = self.get_all_preferences()
        if not prefs:
            return ""
        lines = ["\n[LONG-TERM USER PREFERENCES & MEMORY]"]
        for p in prefs:
            lines.append(f"- {p['category'].upper()}: {p['key']} -> {p['value']}")
        return "\n".join(lines) + "\n"
