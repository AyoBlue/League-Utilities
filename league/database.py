import asyncpg
import typing

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

    # League Team Methods

    async def add_team(self, guild_id: int, team_id: str, logo: typing.Optional[str] = None):
        ...

    async def remove_team(self, guild_id: int, team_id: typing.Optional[str] = None):
        ...

    async def get_team(self, guild_id: int, team_id: str):
        ...

    # League Coach Methods

    async def add_coach(self, guild_id: int, coach_id: int):
        ...

    async def remove_coach(self, guild_id: int, coach_id: typing.Optional[int] = None):
        ...

    async def get_coach_roles(self, guild_id: int):
        ...

    # League Settings Methods

    async def set_setting(self, category: typing.Literal["League", "Channel", "Roles"], guild_id: int, path: str, value: typing.Any):
        ...

    async def get_settings(self, category: typing.Literal["League", "Channel", "Roles"], guild_id: int):
        ...

database = Database()