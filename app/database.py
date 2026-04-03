import logging
import os

import aiomysql

logger = logging.getLogger("backend")

pool: aiomysql.Pool | None = None

MIGRATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "migrations")


async def get_pool() -> aiomysql.Pool:
    global pool
    if pool is None:
        raise RuntimeError("Database pool is not initialized")
    return pool


async def init_db():
    global pool
    pool = await aiomysql.create_pool(
        host=os.environ["MYSQL_HOST"],
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        db=os.environ["MYSQL_DATABASE"],
        maxsize=5,
        autocommit=True,
    )
    await run_migrations()
    logger.info("Database migrations completed successfully")


async def run_migrations():
    migration_files = sorted(
        f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql")
    )
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for filename in migration_files:
                path = os.path.join(MIGRATIONS_DIR, filename)
                with open(path) as f:
                    sql = f.read()
                for statement in sql.split(";"):
                    statement = statement.strip()
                    if statement:
                        await cur.execute(statement)
                logger.info("Applied migration: %s", filename)


async def close_db():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None
