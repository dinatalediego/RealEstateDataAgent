import pandas as pd
from sqlalchemy import text

from config.settings import get_settings
from core.safety import SQLSafetyGuard
from database.supabase_connection import SupabasePostgresConnection


class QueryExecutor:
    def __init__(self, connection: SupabasePostgresConnection, safety_guard: SQLSafetyGuard):
        self.connection = connection
        self.safety_guard = safety_guard
        self.settings = get_settings()

    def run(self, sql: str) -> pd.DataFrame:
        safety = self.safety_guard.validate(sql)
        if not safety.is_safe:
            raise ValueError(safety.reason)

        limited_sql = f"select * from ({sql}) as agent_query limit {self.settings.max_rows}"

        with self.connection.get_engine().connect() as conn:
            return pd.read_sql(text(limited_sql), conn)
