from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    database_url: str
    app_env: str = "local"
    max_rows: int = 500
    show_sql: bool = True


def get_settings() -> Settings:
    load_dotenv()

    database_url = os.getenv("SUPABASE_DATABASE_URL", "")
    app_env = os.getenv("APP_ENV", "local")
    max_rows = int(os.getenv("MAX_ROWS", "500"))
    show_sql = os.getenv("SHOW_SQL", "true").lower() == "true"

    return Settings(
        database_url=database_url,
        app_env=app_env,
        max_rows=max_rows,
        show_sql=show_sql,
    )
