from disnake.ext import commands
import disnake as discord
from datetime import datetime
import psutil
import shared
import json
import sys

bot_emojis = json.load(open('bot_emojis.json'))
class General(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        
    @commands.slash_command(
        description = 'Display Bot Information'
    )
    async def information(self, interaction: discord.ApplicationCommandInteraction):
        process = psutil.Process()
        embed = discord.Embed(
            title = 'League Utilities • Stats',
            description = '',
            colour = 0xFFFFFF,
            timestamp = datetime.now()
        )
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url if interaction.author.display_avatar else None)
        
        embed.add_field('{} Developed By'.format(shared.utils.get_emoji(bot_emojis, 'Developer')), '`ayoblue`', inline=False)
        embed.add_field('{} Python Version'.format(shared.utils.get_emoji(bot_emojis, 'Python')), '{}'.format(sys.version.split()[0]), inline=False)
        embed.add_field('{} Slash Commands'.format(shared.utils.get_emoji(bot_emojis, 'Slash')), len(self.bot.slash_commands), inline=False)
        embed.add_field('{} Uptime'.format(shared.utils.get_emoji(bot_emojis, 'Clock')), '{} Day(s)'.format((datetime.now() - self.started_at).days), inline=False)
        embed.add_field('⌛ CPU Usage', '{}%'.format(psutil.cpu_percent()), inline=True)
        embed.add_field('⌛ Memory Usage', '{:.2f}%'.format(process.memory_percent()), inline=True)

        await interaction.send(embed=embed, components=[
            discord.ui.Button(
                style = discord.ButtonStyle.url,
                label = 'Support Server',
                url = 'https://discord.gg/Cs7rC95j',
                emoji = '🔖'
            )
        ])

    @commands.slash_command(
        description = 'See you or someone elses Profile!',
        options = [
            discord.Option(name='member', type=discord.OptionType.user, required=False)
        ]
    )
    async def profile(self, interaction: discord.ApplicationCommandInteraction, member: discord.Member = None):
        await interaction.response.defer(with_message=True, ephemeral=True)
        if not(member):
            member = interaction.author

        qbbplayer = await shared.database.get_player('QBB', interaction.guild, member)
        embed = discord.Embed(
            title = 'User Profile',
            colour = member.color,
            timestamp = datetime.now()
        )
        embed.set_thumbnail(url=member.display_avatar.url if member.display_avatar else None)
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url if interaction.author.display_avatar else None)
        embed.set_image(url=member._user.banner.url if member._user.banner else interaction.guild.banner.url if interaction.guild.banner else None)

        embed.add_field(name='QBB Review', value='''{} **{}** ({} / {})
{} Wins / {} Losses
{} Games / {}% Win Rate'''.format(
            f'<:{qbbplayer.rank.name}:{qbbplayer.rank.emoji_id}>',
            qbbplayer.rank.name,
            qbbplayer.elo,
            qbbplayer.peak_elo,

            qbbplayer.wins,
            qbbplayer.losses,
            qbbplayer.wins + qbbplayer.losses,
            '0.00' if (qbbplayer.wins + qbbplayer.losses == 0) else '{:.2f}'.join(shared.utils.normalize(qbbplayer.wins, 0, qbbplayer.wins + qbbplayer.losses) * 100)
        ), inline=True)

        league_player = await shared.database.get_player('League', interaction.guild, member)
        value: str = None
        if league_player.role:
            value = f'**Team:** {league_player.emoji} {league_player.role.mention}' if league_player.emoji else f'**Team:** {league_player.role.mention}'
            if league_player.coach:
                value = value + f'\n**Hierachy:** {league_player.coach.mention}'
            else:
                value = value + '\n**Position:** Player'
        else:
            value = 'Free Agent'
        embed.add_field('League Review', value=value, inline=True)

        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))