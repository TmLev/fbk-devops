import os

from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
MIGRATIONS_DIR = SRC_DIR / "migrations"


class HistorianConfig:

    def __init__(self) -> None:
        self.port = int(os.environ["HISTORIAN_PORT"])
        secs = os.environ["HISTORIAN_MIGRATIONS_TIMEOUT_SECS"]
        self.migrations_timeout = int(secs)


HISTORIAN_CONFIG = HistorianConfig()


class PostgresConfig:

    def __init__(self) -> None:
        self.host = os.environ["POSTGRES_HOST"]
        self.port = int(os.environ["POSTGRES_PORT"])
        self.db = os.environ["POSTGRES_DB"]
        self.user = os.environ["POSTGRES_USER"]
        self.password = os.environ["POSTGRES_PASSWORD"]

        self.url = (f"postgresql://{self.user}:{self.password}"
                    f"@{self.host}:{self.port}/{self.db}")


POSTGRES_CONFIG = PostgresConfig()
