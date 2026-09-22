import aiosqlite as db
from aiosqlite import Connection as conn

async def connect_db():
    conn = await db.connect('./database/url.db')
    await conn.execute("PRAGMA journal_mode=WAL;")
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS urls(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)
    await conn.commit()
    return conn

async def get_id(conn: conn, url: str):
    cur = await conn.cursor()
    query = await cur.execute(
        """
            SELECT id
            FROM urls
            WHERE url = ?;
        """, (url, ))
    result = await query.fetchone()
    if result is None:
        return None
    return result[0]

async def add_url(conn: conn, url: str):
    cur = await conn.cursor()
    await cur.execute(
         """
            INSERT INTO urls(url) VALUES(?);
        """, (url, ))
    await conn.commit()

async def get_url(conn: conn, id: str):
    cur = await conn.cursor()
    query = await cur.execute(
        """
            SELECT url
            FROM urls
            WHERE id = ?;
        """, (id, ))
    result = await query.fetchone()
    if result is None:
        return None
    return result[0]
