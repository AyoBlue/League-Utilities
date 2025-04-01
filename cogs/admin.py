from disnake.ext import commands
import disnake as discord
from datetime import datetime

class Admin(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.started_at = datetime.now()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not(message.guild.id == 1307571123726323813):
            return
        if not(message.author.id == 365499293357834240):
            return

def setup(bot):
    bot.add_cog(Admin(bot))