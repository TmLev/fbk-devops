import uvicorn
import yoyo

from fastapi import FastAPI

from proto import Entry
from repo import PostgresRepo
from config import (
    HISTORIAN_CONFIG,
    POSTGRES_CONFIG,
    MIGRATIONS_DIR,
)

historian = FastAPI()
repo = PostgresRepo()


@historian.post("/entries/")
async def post_entry(entry: Entry):
    data = entry.data
    id_ = await repo.write_entry(data)
    return {
        "id": id_,
    }


@historian.get("/__tests/entries/{id_}/")
async def get_entry(id_: int) -> Entry:
    data = await repo.read_entry(id_)
    return Entry(data=data)


def run_migrations() -> None:
    backend = yoyo.get_backend(POSTGRES_CONFIG.url)
    migrations = yoyo.read_migrations(str(MIGRATIONS_DIR))
    with backend.lock(timeout=HISTORIAN_CONFIG.migrations_timeout):
        backend.apply_migrations(backend.to_apply(migrations))


if __name__ == "__main__":
    run_migrations()

    uvicorn.run(
        "main:historian",
        host="0.0.0.0",
        port=HISTORIAN_CONFIG.port,
        reload=True,
    )
