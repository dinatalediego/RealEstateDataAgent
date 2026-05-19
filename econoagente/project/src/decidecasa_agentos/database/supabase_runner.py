from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine, text

from decidecasa_agentos.core.models import QueryDefinition
from decidecasa_agentos.database.demo_data import get_demo_data
from decidecasa_agentos.utils.settings import AppSettings


class ConnectionHealthCheck:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    def status(self) -> tuple[bool, str]:
        if self.settings.is_demo:
            return True, "Modo demo activo: usando datos de ejemplo."
        try:
            engine = create_engine(self.settings.database_url, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text("select 1"))
            return True, "Conexión Supabase/Postgres OK."
        except Exception as exc:  # noqa: BLE001
            return False, f"Error de conexión: {exc}"


class SupabaseQueryRunner:
    """Ejecuta SQL aprobado contra Supabase/Postgres o demo data."""

    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings
        self.engine = None if settings.is_demo else create_engine(settings.database_url, pool_pre_ping=True)

    def run(self, query: QueryDefinition, safe_sql: str) -> pd.DataFrame:
        if self.settings.is_demo:
            return get_demo_data(query.id)
        assert self.engine is not None
        with self.engine.connect() as conn:
            conn.execute(text(f"set statement_timeout = {self.settings.query_timeout_seconds * 1000}"))
            return pd.read_sql(text(safe_sql), conn)
