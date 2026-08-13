import asyncpg
import typing
import os

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS league_teams (
    guild_id BIGINT PRIMARY KEY,
    team_id BIGINT NOT NULL,
    logo_id BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS league_coaches (
    guild_id BIGINT PRIMARY KEY,
    coach_id BIGINT NOT NULL
);
"""

ADD_TEAM = """
WITH add_team AS (
    INSERT INTO league_teams (guild_id, team_id, logo_id)
    VALUES ($1, $2, $3)
    ON CONFLICT (guild_id) DO NOTHING
);
"""

REMOVE_TEAM = """

"""

ADD_COACH = """

"""

REMOVE_COACH = """

"""

SET_CHANNEL_SETTING = """

"""

SET_LEAGUE_SETTING = """

"""

SET_ROLE_SETTING = """

"""

class Database:
    def __init__(self):
        self.pool: asyncpg.Pool = None

    async def connect(self):
        if self.pool is not None:
            return self.pool

        self.pool = await asyncpg.create_pool(
            database = "leagueutilities",
            host = os.getenv("HOST_URL"),
            port = 5432,
            user = os.getenv("HOST_USER"),
            password = os.getenv("HOST_PASSWORD"),
            min_size = 1,
            max_size = 100
        )
        await self.pool.execute(CREATE_TABLES)

    async def close(self):
        if self.pool is not None:
            await self.pool.close()

    async def get_pool(self) -> asyncpg.Pool:
        if self.pool is None:
            raise Exception("Database connection pool is not initialized.")
        
        return self.pool

    # League Team Methods

    async def add_team(self, guild_id: int, team_id: str, logo_id: typing.Optional[int] = None):
        pool = await self.get_pool()
        pool.execute(ADD_TEAM, guild_id, team_id, logo_id or 0)

    async def remove_team(self, guild_id: int, team_id: typing.Optional[int] = None):
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