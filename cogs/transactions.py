from disnake.ext import commands
import disnake as discord

class Transactions(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        
    @commands.slash_command(
        description = 'Offer a player!',
        options = [
            discord.Option(name='member', type=discord.OptionType.user, required=True)
        ]
    )
    async def offer(self, interaction: discord.ApplicationCommandInteraction, **args):
        await interaction.response.defer(ephemeral=True)

    @commands.slash_command(
        description = 'Release a player from your team!',
        options = [
            discord.Option(name='member', type=discord.OptionType.user, required=True)
        ]
    )
    async def release(self, interaction: discord.ApplicationCommandInteraction, member: discord.Member):
        await interaction.response.defer(ephemeral=True)

    @commands.slash_command(
        description = 'Promote a player on your team!',
        options = [
            discord.Option(name='member', type=discord.OptionType.user, required=True),
            discord.Option(name='role', type=discord.OptionType.role, required=True)
        ]
    )
    async def promote(self, interaction: discord.ApplicationCommandInteraction, member: discord.Member, role: discord.Role):
        await interaction.response.defer(ephemeral=True)

    @commands.slash_command(
        description = 'Demote a player on your team!',
        options = [
            discord.Option(name='member', type=discord.OptionType.user, required=True)
        ]
    )
    async def demote(self, interaction: discord.ApplicationCommandInteraction, member: discord.Member):
        await interaction.response.defer(ephemeral=True)

    @commands.slash_command(
        description = 'Demand from your team!'
    )
    async def demand(self, interaction: discord.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

def setup(bot):
    bot.add_cog(Transactions(bot))