import re
import subprocess
from typing import Dict, Any, Tuple, List

class RiskLevel:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Guardian:
    """Security and Risk assessment gatekeeper."""

    @staticmethod
    def assess_diff(repo_path: str, diff_text: str) -> Tuple[str, List[str]]:
        risks = []
        lines = diff_text.splitlines()

        deleted_lines = [l for l in lines if l.startswith("-") and not l.startswith("---")]
        added_lines = [l for l in lines if l.startswith("+") and not l.startswith("+++")]

        # Check for signature changes (def / class / public methods)
        for line in deleted_lines:
            if re.search(r'^\-\s*(def|class|async def)\s+[a-zA-Z0-9_]+', line):
                risks.append(f"Public API or function signature deleted/modified: `{line.strip()}`")
            if re.search(r'^\-\s*(DROP|DELETE FROM|ALTER TABLE)', line, re.IGNORECASE):
                risks.append(f"Database schema/data deletion risk: `{line.strip()}`")

        # Check if entire files or large blocks were deleted (> 30 lines)
        if len(deleted_lines) > 40:
            risks.append(f"Large deletion block ({len(deleted_lines)} lines removed)")

        # Determine level
        if any("Public API" in r or "Database" in r for r in risks):
            return RiskLevel.HIGH, risks
        elif len(risks) > 0:
            return RiskLevel.MEDIUM, risks
        else:
            return RiskLevel.LOW, ["Bug fix / internal implementation change only (safe)"]
