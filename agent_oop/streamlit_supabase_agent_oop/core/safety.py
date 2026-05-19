import re
from dataclasses import dataclass
from typing import List


@dataclass
class SafetyResult:
    is_safe: bool
    reason: str = ""


class SQLSafetyGuard:
    """
    Validador defensivo. No reemplaza permisos de base de datos.
    Idealmente usar un usuario read-only en Supabase/Postgres.
    """

    FORBIDDEN_PATTERNS: List[str] = [
        r"\binsert\b",
        r"\bupdate\b",
        r"\bdelete\b",
        r"\bdrop\b",
        r"\btruncate\b",
        r"\balter\b",
        r"\bcreate\b",
        r"\bgrant\b",
        r"\brevoke\b",
        r"\bcopy\b",
        r"\bexecute\b",
        r";\s*\w+",
    ]

    def validate(self, sql: str) -> SafetyResult:
        normalized = sql.lower().strip()

        if not normalized.startswith("select"):
            return SafetyResult(False, "Solo se permiten consultas SELECT.")

        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, normalized, flags=re.IGNORECASE):
                return SafetyResult(False, f"SQL bloqueado por patrón no permitido: {pattern}")

        return SafetyResult(True, "SQL seguro para ejecución read-only.")
