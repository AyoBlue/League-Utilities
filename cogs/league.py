from disnake.ext import commands
import disnake as discord

class League(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(
        description = 'Disband a team!',
        options = [
            discord.Option(name='team', type=discord.OptionType.role, required=True)
        ]
    )
    async def disband(self, interaction: discord.ApplicationCommandInteraction, team: discord.Role):
        ...

    @commands.slash_command(
        description = 'Appoint a player as owner of a team!',
        options = [
            discord.Option(name='team', type=discord.OptionType.role, required=True),
            discord.Option(name='member', type=discord.OptionType.user, required=True),
        ]
    )
    async def appoint(self, interaction: discord.ApplicationCommandInteraction, team: discord.Role, member: discord.Member):
        ...


def setup(bot):
    bot.add_cog(League(bot))