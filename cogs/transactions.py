from discord.ext import commands
from discord import app_commands
import discord

class Transactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="offer")
    @app_commands.guild_only()
    async def offer(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(ephmeral=True)

    @app_commands.command(name="release")
    @app_commands.guild_only()
    async def release(self, interaction: discord.Interaction, member: discord.Member):
        ...

    @app_commands.command(name="promote")
    @app_commands.guild_only()
    async def promote(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        ...

    @app_commands.command(name="demote")
    @app_commands.guild_only()
    async def demote(self, interaction: discord.Interaction, member: discord.Member):
        ...

    @app_commands.command(name="demand")
    @app_commands.guild_only()
    async def demand(self, interaction: discord.Interaction):
        ...

async def setup(bot: commands.Bot):
    await bot.add_cog(Transactions(bot))