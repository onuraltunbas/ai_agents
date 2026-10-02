import os
import re
import shutil
import subprocess
from typing import Tuple, Dict, Any, Optional

def extract_clean_code(text: str, language: str = "python") -> str:
    """Extract code block from markdown LLM response."""
    pattern = rf"```{language}\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    pattern_generic = r"```\s*\n(.*?)```"
    match = re.search(pattern_generic, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

class CodeVerifier:
    """Zero-Defect Multi-Stage Code Verification Pipeline (Ruff + Mypy + Pytest)."""

    @staticmethod
    def get_bin(cmd: str) -> str:
        found = shutil.which(cmd)
        if found:
            return found
        home_local = os.path.expanduser(f"~/.local/bin/{cmd}")
        if os.path.exists(home_local):
            return home_local
        return cmd

    @classmethod
    def verify(
        cls,
        target_file: str,
        test_dir: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        results: Dict[str, Any] = {}
        ruff_bin = cls.get_bin("ruff")
        mypy_bin = cls.get_bin("mypy")
        pytest_bin = cls.get_bin("pytest")

        # 1. Ruff linting
        res_ruff = subprocess.run([ruff_bin, "check", target_file], capture_output=True, text=True)
        results["ruff"] = (res_ruff.returncode == 0)
        results["ruff_out"] = res_ruff.stdout + res_ruff.stderr

        # 2. Mypy type checking
        res_mypy = subprocess.run([mypy_bin, "--ignore-missing-imports", target_file], capture_output=True, text=True)
        results["mypy"] = (res_mypy.returncode == 0)
        results["mypy_out"] = res_mypy.stdout + res_mypy.stderr

        # 3. Pytest test suite
        if test_dir and os.path.exists(test_dir):
            res_pytest = subprocess.run([pytest_bin, test_dir], capture_output=True, text=True, env=env)
            results["pytest"] = (res_pytest.returncode == 0)
            results["pytest_out"] = res_pytest.stdout + res_pytest.stderr
        else:
            results["pytest"] = True
            results["pytest_out"] = "No tests directory provided."

        all_passed = bool(results["ruff"] and results["mypy"] and results["pytest"])
        return all_passed, results
