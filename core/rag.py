import urllib.request
import json
import sqlite3
import os
import math
from typing import List, Dict, Any, Tuple

OLLAMA_EMBED_API = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
DB_PATH = "/home/onur/.onur_ai/rag_index.db"

def get_embedding(text: str) -> List[float]:
    payload = {"model": EMBED_MODEL, "prompt": text}
    req = urllib.request.Request(
        OLLAMA_EMBED_API,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("embedding", [])

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

class LocalRAG:
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT,
                chunk_index INTEGER,
                content TEXT,
                embedding_json TEXT
            )
            """)

    def index_directory(self, dir_path: str, extensions: List[str] = [".py", ".c", ".h", ".cpp", ".xml", ".md"]):
        with self.conn:
            self.conn.execute("DELETE FROM chunks WHERE file_path LIKE ?", (f"{dir_path}%",))
            
        count = 0
        for root, _, files in os.walk(dir_path):
            if "/.git" in root or "/__pycache__" in root:
                continue
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext in extensions:
                    full_path = os.path.join(root, f)
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                    
                    # Index in chunks
                    chunk_size = 1000
                    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
                    for idx, ch in enumerate(chunks):
                        if not ch.strip():
                            continue
                        emb = get_embedding(ch)
                        with self.conn:
                            self.conn.execute("""
                            INSERT INTO chunks (file_path, chunk_index, content, embedding_json)
                            VALUES (?, ?, ?, ?)
                            """, (full_path, idx, ch, json.dumps(emb)))
                        count += 1
        return count

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        q_emb = get_embedding(query)
        cursor = self.conn.cursor()
        cursor.execute("SELECT file_path, chunk_index, content, embedding_json FROM chunks")
        rows = cursor.fetchall()
        
        scored = []
        for r in rows:
            emb = json.loads(r[3])
            score = cosine_similarity(q_emb, emb)
            scored.append({"file_path": r[0], "chunk": r[1], "content": r[2], "score": score})
            
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
