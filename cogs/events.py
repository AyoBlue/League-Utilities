from disnake.ext import commands
import disnake as discord
import shared

class Events(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Events(bot))