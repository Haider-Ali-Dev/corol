import asyncio

import asyncpg

loop = asyncio.get_event_loop()
CONNECTION_URL = "postgres://haider@localhost:5432/corol"


async def create_connection():
    return await asyncpg.connect("postgres://haider@localhost:5432/corol")


class Database():
    connection = None

    def __init__(self, connection_url) -> None:
        self.connection_url = connection_url

    async def connect(self):
        self.connection = await asyncpg.connect(self.connection_url)
        return self

    async def close(self):
        await self.connection.close()

    async def get_results(self, term: str):
        data = await self.connection.fetch("""
SELECT * FROM page LIMIT 500


        """)
        return data
