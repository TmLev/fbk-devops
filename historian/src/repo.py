import asyncpg

from config import POSTGRES_CONFIG


class PostgresRepo:

    def __init__(self) -> None:
        self._pool = asyncpg.create_pool(dsn=POSTGRES_CONFIG.url)
        self._initialized_pool = False

    async def _initialize_pool(self) -> None:
        self._pool = await self._pool
        self._initialized_pool = True

    async def write_entry(self, entry: str) -> int:
        if not self._initialized_pool:
            await self._initialize_pool()

        id_ = await self._pool.fetchval(
            "INSERT INTO history (entry) VALUES($1) "
            "RETURNING id",
            entry,
        )

        return int(id_)

    async def read_entry(self, id_: int) -> str:
        if not self._initialized_pool:
            await self._initialize_pool()

        entry = await self._pool.fetchval(
            "SELECT entry FROM history "
            "WHERE id = $1",
            id_,
        )

        return entry
