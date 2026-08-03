from discord.ext import commands
import discord
import league
import os

from dotenv import load_dotenv
load_dotenv()

class LeagueBot(commands.Bot):
    async def setup_hook(self):
        await league.database.connect()

        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file[:-3]}")

        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})\nWatching over {len(self.guilds)} guild(s)")

    async def close(self):
        await league.database.close()
        await super().close()

bot = LeagueBot(command_prefix="!", intents=discord.Intents().all())
token = os.getenv("DISCORD_TOKEN", os.environ["DISCORD_TOKEN"])

print(token)
bot.run(token)