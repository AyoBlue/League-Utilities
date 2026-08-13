from discord.ext import commands
from discord import app_commands
import discord

class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="")
    @app_commands.guild_only()
    async def name_(self, interaction: discord.Interaction):
        ...

async def setup(bot: commands.Bot):
    await bot.add_cog(Server(bot))