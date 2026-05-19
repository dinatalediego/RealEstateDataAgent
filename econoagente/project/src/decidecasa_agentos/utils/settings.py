from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppSettings:
    app_mode: str
    database_url: str | None
    allowed_schemas: tuple[str, ...]
    max_rows: int
    query_timeout_seconds: int
    log_path: Path

    @property
    def is_demo(self) -> bool:
        return self.app_mode.lower() == "demo" or not self.database_url


def load_settings() -> AppSettings:
    load_dotenv()
    allowed = os.getenv("AGENT_ALLOWED_SCHEMAS", "gold,mart,public")
    return AppSettings(
        app_mode=os.getenv("APP_MODE", "demo"),
        database_url=os.getenv("SUPABASE_DATABASE_URL") or None,
        allowed_schemas=tuple(x.strip() for x in allowed.split(",") if x.strip()),
        max_rows=int(os.getenv("AGENT_MAX_ROWS", "500")),
        query_timeout_seconds=int(os.getenv("AGENT_QUERY_TIMEOUT_SECONDS", "20")),
        log_path=Path(os.getenv("AGENT_LOG_PATH", "logs/query_audit.csv")),
    )
