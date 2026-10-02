import os
import sys
import json
import time
import re
import subprocess
import urllib.request

from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from memory import MemoryEngine
from guardian import Guardian, RiskLevel
from rag import LocalRAG
from verifier import CodeVerifier, extract_clean_code

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3-coder:30b"

def call_local_model(prompt: str, system: str = "") -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.85,
            "num_ctx": 65536
        }
    }
    req = urllib.request.Request(
        OLLAMA_API,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("response", "")

def run_agent_workflow(repo_path: str, user_instruction: str):
    print("="*75)
    print("🤖 ONUR AI UNIFIED AGENT & ORCHESTRATOR")
    print("="*75)
    
    # 1. Initialize Long-Term Memory
    memory = MemoryEngine()
    memory.set_preference("architecture", "concurrency", "Prefer atomic/lock-free or clear thread-safe semantics")
    memory.set_preference("python", "typing", "Always enforce type hints and dataclasses")
    memory.set_preference("safety", "risk_gate", "Always ask before modifying public APIs or database schemas")
    memory.set_preference("testing", "zero_defect", "Code must pass pytest and ruff before commit")
    
    mem_prompt = memory.get_context_prompt_fragment()
    print(f"🧠 [Memory] Loaded {len(memory.get_all_preferences())} persistent preferences from SQLite.")
    
    # 2. Index Repository via Local RAG (nomic-embed-text)
    print("📚 [RAG] Indexing repository with local nomic-embed-text embeddings...")
    rag = LocalRAG()
    num_chunks = rag.index_directory(repo_path)
    print(f"✅ [RAG] Indexed {num_chunks} code chunks into local vector database.")
    
    # 3. Perform Semantic Retrieval
    search_query = "Kalman filter angle normalization wrap around innovation"
    rag_results = rag.search(search_query, top_k=2)
    print(f"🔍 [RAG] Semantic search for '{search_query}':")
    for r in rag_results:
        print(f"   -> {os.path.basename(r['file_path'])} (similarity: {r['score']:.3f})")
    
    # 4. Run Pytest to capture exact failure before fix
    pytest_bin = CodeVerifier.get_bin("pytest")
    ruff_bin = CodeVerifier.get_bin("ruff")
    mypy_bin = CodeVerifier.get_bin("mypy")

    print("\n🧪 [Verifier] Running initial test suite...")
    env = os.environ.copy()
    env["PYTHONPATH"] = repo_path
    res_test = subprocess.run([pytest_bin, os.path.join(repo_path, "tests")], capture_output=True, text=True, env=env)
    
    # 5. Agent Diagnosis and Fix Prompt
    target_file = os.path.join(repo_path, "src/sensor_fusion.py")
    if not os.path.exists(target_file):
        # Fallback to any python file if run in a generic directory
        py_files = [os.path.join(r, f) for r, _, fs in os.walk(repo_path) for f in fs if f.endswith(".py") and "test" not in f]
        target_file = py_files[0] if py_files else os.path.join(repo_path, "main.py")

    with open(target_file, "r") as f:
        original_code = f.read()
        
    prompt = f"""
{mem_prompt}

REPOSITORY CONTEXT:
Target file: {os.path.relpath(target_file, repo_path)}
Content:
```python
{original_code}
```

TEST FAILURE DIAGNOSTICS:
\"\"\"
{res_test.stdout}
\"\"\"

USER GOAL:
{user_instruction}

INSTRUCTIONS:
1. Fix the issues identified in diagnostics and achieve the user goal.
2. Maintain all type hints and dataclass definitions. Do NOT leave unused imports.
3. Return the COMPLETE fixed file in a ```python ... ``` code block.
"""
    print("⏳ [Local LLM] Generating fix with Qwen3-Coder 30B (64K context)...")
    t0 = time.time()
    ai_response = call_local_model(prompt, "You are a senior ROS2 & robotics software engineer. Write clean, lint-free Python code.")
    t1 = time.time()
    print(f"⏱️ Model completed in {t1 - t0:.2f} seconds.")
    
    new_code = extract_clean_code(ai_response, "python")
    with open(target_file, "w") as f:
        f.write(new_code)
        
    # Auto-format / fix lints with ruff
    subprocess.run([ruff_bin, "check", "--fix", target_file], capture_output=True, text=True)
    subprocess.run([ruff_bin, "format", target_file], capture_output=True, text=True)
        
    # 6. Guardian Risk Assessment on Git Diff
    diff_res = subprocess.run(["git", "-C", repo_path, "diff"], capture_output=True, text=True)
    risk_level, risk_details = Guardian.assess_diff(repo_path, diff_res.stdout)
    print(f"\n🛡️ [Guardian] Risk Assessment: {risk_level}")
    for r in risk_details:
        print(f"   - {r}")
        
    # 7. Multi-Stage Verification Pipeline (AST + Ruff + Mypy + Pytest)
    print("\n🔬 [Verifier] Running Multi-Stage Verification Pipeline...")
    res_ruff = subprocess.run([ruff_bin, "check", target_file], capture_output=True, text=True)
    res_mypy = subprocess.run([mypy_bin, "--ignore-missing-imports", target_file], capture_output=True, text=True)
    res_pytest = subprocess.run([pytest_bin, os.path.join(repo_path, "tests")], capture_output=True, text=True, env=env)
    
    if res_pytest.returncode == 0 and res_ruff.returncode == 0 and res_mypy.returncode == 0:
        print("🎉 ALL TESTS, RUFF LINTER & MYPY PASSED 100% (ZERO DEFECTS)!")
        print("\n" + "="*45 + " GIT DIFF " + "="*45)
        print(diff_res.stdout)
        print("="*100)
        
        # Record successful decision in memory
        memory.record_decision(os.path.basename(repo_path), "Autonomous code fix applied and verified", "Passed Ruff, Mypy and Pytest", True)
        print("💾 [Memory] Recorded verified solution into long-term memory database.")
        return True
    else:
        print("❌ Verification failed:")
        if res_pytest.returncode != 0: print("Pytest:\n", res_pytest.stdout)
        if res_ruff.returncode != 0: print("Ruff:\n", res_ruff.stdout)
        if res_mypy.returncode != 0: print("Mypy:\n", res_mypy.stdout)
        return False

if __name__ == "__main__":
    target_repo = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    goal = sys.argv[2] if len(sys.argv) > 2 else "Fix tests and ensure zero defects."
    run_agent_workflow(target_repo, goal)
