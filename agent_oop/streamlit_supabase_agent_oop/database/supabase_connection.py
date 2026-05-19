from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config.settings import get_settings


class SupabasePostgresConnection:
    def __init__(self):
        self.settings = get_settings()
        if not self.settings.database_url:
            raise ValueError(
                "Falta SUPABASE_DATABASE_URL. Copia .env.example como .env y completa la conexión."
            )
        self.engine: Engine = create_engine(self.settings.database_url, pool_pre_ping=True)

    def get_engine(self) -> Engine:
        return self.engine
