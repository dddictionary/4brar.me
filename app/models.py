import aiomysql


async def get_all_posts(pool: aiomysql.Pool) -> list[dict]:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT id, name, email, content, created_at FROM timelinepost ORDER BY created_at DESC"
            )
            rows = await cur.fetchall()
            for row in rows:
                row["created_at"] = row["created_at"].isoformat()
            return rows


async def create_post(pool: aiomysql.Pool, name: str, email: str, content: str) -> dict:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "INSERT INTO timelinepost (name, email, content) VALUES (%s, %s, %s)",
                (name, email, content),
            )
            post_id = cur.lastrowid
            await cur.execute(
                "SELECT id, name, email, content, created_at FROM timelinepost WHERE id = %s",
                (post_id,),
            )
            row = await cur.fetchone()
            row["created_at"] = row["created_at"].isoformat()
            return row
