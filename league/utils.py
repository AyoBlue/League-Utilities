from .database import database
import definitions
import discord

class Utils:
    def __init__(self):
        self.database = database

    async def get_team(self, team_id: int):
        ...

    async def get_teams(self, guild: discord.Guild):
        ...

    async def get_player(self, member: discord.Member):
        ...

utils = Utils()