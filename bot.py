import disnake as discord
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot = commands.InteractionBot(intents=discord.Intents().all())

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(os.environ['TOKEN'])