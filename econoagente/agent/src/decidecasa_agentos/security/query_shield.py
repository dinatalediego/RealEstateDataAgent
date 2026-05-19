from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ShieldResult:
    allowed: bool
    sql: str | None
    reason: str | None = None


class QueryShield:
    """Cinturón de seguridad: solo SELECT, esquemas autorizados y límite de filas."""

    forbidden_patterns = [
        r"\binsert\b", r"\bupdate\b", r"\bdelete\b", r"\bdrop\b", r"\btruncate\b",
        r"\balter\b", r"\bcreate\b", r"\bgrant\b", r"\brevoke\b", r"\bcopy\b",
        r"\bcall\b", r"\bexecute\b", r"\bdo\b", r"\bmerge\b",
    ]

    def __init__(self, allowed_schemas: tuple[str, ...], max_rows: int = 500) -> None:
        self.allowed_schemas = allowed_schemas
        self.max_rows = max_rows

    def validate(self, sql: str) -> ShieldResult:
        clean = self._clean_sql(sql)
        lowered = clean.lower()

        if not lowered.startswith("select") and not lowered.startswith("with"):
            return ShieldResult(False, None, "Solo se permiten consultas SELECT o WITH.")

        for pattern in self.forbidden_patterns:
            if re.search(pattern, lowered):
                return ShieldResult(False, None, f"Comando no permitido detectado: {pattern}")

        schemas = set(re.findall(r"\b([a-zA-Z_][\w]*)\.[a-zA-Z_][\w]*\b", clean))
        unauthorized = schemas.difference(set(self.allowed_schemas))
        if unauthorized:
            return ShieldResult(False, None, f"Esquemas no autorizados: {', '.join(sorted(unauthorized))}")

        clean = self._ensure_limit(clean)
        return ShieldResult(True, clean, None)

    def _clean_sql(self, sql: str) -> str:
        return sql.strip().rstrip(";")

    def _ensure_limit(self, sql: str) -> str:
        if re.search(r"\blimit\s+\d+\b", sql.lower()):
            return sql
        return f"{sql}\nlimit {self.max_rows}"
