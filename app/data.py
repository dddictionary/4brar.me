import aiomysql

NAV_ITEMS = [
    {"href": "/aboutme", "caption": "About Me"},
    {"href": "/work", "caption": "Work Experiences"},
    {"href": "/hobbies", "caption": "Hobbies"},
    {"href": "/education", "caption": "Education"},
    {"href": "/travels", "caption": "Travels"},
    {"href": "/timeline", "caption": "Timeline"},
]


async def get_hobbies(pool: aiomysql.Pool) -> list[dict]:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT title, description, source FROM hobbies ORDER BY id")
            return await cur.fetchall()


async def get_work_experiences(pool: aiomysql.Pool) -> list[dict]:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT title, role, startdate, enddate, description FROM work_experiences ORDER BY id"
            )
            return await cur.fetchall()


async def get_education(pool: aiomysql.Pool) -> list[dict]:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT title, startdate, enddate, description FROM education ORDER BY id"
            )
            return await cur.fetchall()


async def get_locations(pool: aiomysql.Pool) -> list[dict]:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT name, lat, lng FROM locations ORDER BY id")
            return await cur.fetchall()
