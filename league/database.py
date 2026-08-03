import asyncpg

class Database:
    def __init__(self):
        self.pool: asyncpg.Pool = None

    async def connect(self):
        ...

    async def close(self):
        ...

    async def get_pool(self) -> asyncpg.Pool:
        if self.pool is None:
            raise Exception("Database connection pool is not initialized.")
        
        return self.pool

database = Database()