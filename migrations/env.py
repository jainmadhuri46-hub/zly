
import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection, make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app import models  # noqa: F401
from app.db import Base


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_database_url():
    raw_url = os.environ.get("DATABASE_URL")

    if not raw_url or not raw_url.strip():
        raise RuntimeError(
            "DATABASE_URL is missing or empty. "
            "Check Railway service variables."
        )

    raw_url = raw_url.strip()

    if raw_url.startswith("${{"):
        raise RuntimeError(
            "DATABASE_URL contains an unresolved Railway variable reference."
        )

    try:
        url = make_url(raw_url)
    except Exception as exc:
        raise RuntimeError(
            "DATABASE_URL is not a valid database URL."
        ) from exc

    if url.drivername in ("postgresql", "postgres"):
        url = url.set(drivername="postgresql+asyncpg")

    if url.drivername != "postgresql+asyncpg":
        raise RuntimeError(
            "DATABASE_URL must use PostgreSQL with the asyncpg driver."
        )

    if not url.host or not url.database or not url.username:
        raise RuntimeError(
            "DATABASE_URL is missing its host, database, or username."
        )

    return url


def run_migrations_offline() -> None:
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    url = get_database_url()

    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )

    try:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
