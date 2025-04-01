from typing import Literal, Union
from datetime import datetime, timedelta
from disnake.ext import commands
import disnake as discord
import shared

class Settings(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    # Team Management

    @commands.slash_command()
    async def team(self, interaction: discord.ApplicationCommandInteraction):
        ...

    @team.sub_command(
        description = 'Add a team!',
        options = [
            discord.Option(name='team', type=discord.OptionType.role, required=True),
            discord.Option(name='emoji', type=discord.OptionType.string, required=False)
        ]
    )
    async def add(self, interaction: discord.ApplicationCommandInteraction, team: discord.Role, emoji: str = None):
        await interaction.response.defer(with_message=True, ephemeral=True)
        if emoji:
            try:
                emoji: discord.Emoji = discord.utils.get(interaction.guild.emojis, id=int(''.join(filter(str.isdigit, emoji))))
            except:
                return await interaction.send(f'{emoji} is not a valid emoji.')

        boolean = await shared.database.add_team(server=interaction.guild, team=team, emoji=emoji)
        if not(interaction.author.guild_permissions.administrator):
            await interaction.send('You do not have permission to use this command.')
        elif team.position >= interaction.author.top_role.position:
            await interaction.send('You cannot use this role due to role hierachy.')
        elif boolean == 'Max':
            embed = discord.Embed(
                title = 'Max Teams',
                description = 'You have reached the max amount of teams you are allowed to have.',
                colour = shared.utils.decline['color'],
                timestamp = datetime.now()
            )
            embed.set_author(name='{} • Error'.format(interaction.guild.name), icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url)

            await interaction.send(embed=embed)
        elif boolean == 'Exists':
            embed = discord.Embed(
                title = 'Team Exists',
                description = '{} is already an existing team.'.format(team.mention),
                colour = shared.utils.decline['color'],
                timestamp = datetime.now()
            )
            embed.set_author(name='{} • Error'.format(interaction.guild.name), icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url)

            await interaction.send(embed=embed)
        else:
            embed = discord.Embed(
                title = 'Team Added',
                description = 'You have successfully added {} as a team!'.format(
                    (f'{emoji} ' if emoji else '') + team.mention
                ),
                colour = team.color,
                timestamp = datetime.now()
            )
            embed.set_author(name='{} • Team Management'.format(interaction.guild.name), icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url)
            if emoji:
                embed.set_thumbnail(url=emoji.url)

            await interaction.send(embed=embed)

    @team.sub_command(
        description = 'Add a team!',
        options = [
            discord.Option(name='team', type=discord.OptionType.role, required=True)
        ]
    )
    async def remove(self, interaction: discord.ApplicationCommandInteraction, team: discord.Role):
        await interaction.response.defer(with_message=True, ephemeral=True)

        if not(interaction.author.guild_permissions.administrator):
            await interaction.send('You do not have permission to use this command.')
        elif not(await shared.database.get_team(interaction.guild, team)):
            await interaction.send('{} is not a valid team.'.format(team.mention))
        else:
            await shared.database.remove_team(interaction.guild, team)
            embed = discord.Embed(
                title = 'Team Removed',
                description = 'You have successfully removed {} from your servers teams!'.format(team.mention),
                colour = team.color,
                timestamp = datetime.now()
            )
            embed.set_author(name='{} • Team Management'.format(interaction.guild.name), icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url)

            await interaction.send(embed=embed)

    # Coach Management

    @commands.slash_command()
    async def coach(self, interaction: discord.ApplicationCommandInteraction):
        ...

    @coach.sub_command(
        name = 'add',
        description = 'Add a coach role!',
        options = [
            discord.Option(name='role', type=discord.OptionType.role, required=True),
            discord.Option(name='limit', description='Member Limit with Role on a Team.', type=discord.OptionType.integer, required=False)
        ]
    )
    async def coach__add(self, interaction: discord.ApplicationCommandInteraction, role: discord.Role, limit: int = 1):
        await interaction.response.defer(with_message=True, ephemeral=True)

        if not(interaction.author.guild_permissions.administrator):
            await interaction.send('You do not have permission to use this command.')
        elif role.position >= interaction.author.top_role.position:
            await interaction.send('You cannot use this role due to role hierachy.')
        elif (await shared.database.get_coach(interaction.guild, role)):
            await interaction.send('{} is already a coach role.'.format(role.mention))
        else:
            await shared.database.add_coach(interaction.guild, role, limit)
            embed = discord.Embed(
                title = 'Coach Added',
                description = 'You have successfully added {} as a coach role!'.format(role.mention),
                color = shared.utils.accept['color'],
                timestamp = datetime.now()
            )
            embed.set_author(name='{} • Coach Management'.format(interaction.guild.name), icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url)

            await interaction.send(embed=embed)

    @coach.sub_command(
        name = 'remove',
        description = 'Remove a coach role!',
        options = [
            discord.Option(name='role', type=discord.OptionType.role, required=True)
        ]
    )
    async def coach__remove(self, interaction: discord.ApplicationCommandInteraction, role: discord.Role):
        await interaction.response.defer(with_message=True, ephemeral=True)

        if not(interaction.author.guild_permissions.administrator):
            await interaction.send('You do not have permission to use this command.')
        elif not(await shared.database.get_coach(interaction.guild, role)):
            await interaction.send('{} is not a coach role.'.format(role.mention))
        else:
            await shared.database.remove_coach(interaction.guild, role)
            embed = discord.Embed(
                title = 'Coach Removed',
                description = 'You have successfully removed {} as a coach role!'.format(role.mention),
                color = shared.utils.accept['color'],
                timestamp = datetime.now()
            )
            embed.set_author(name='{} • Coach Management'.format(interaction.guild.name), icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url)

            await interaction.send(embed=embed)

    # Role Management

    @commands.slash_command()
    async def role(self, interaction: discord.ApplicationCommandInteraction):
        ...

    @role.sub_command(
        name = 'set',
        options = [
            discord.Option(name='section', type=discord.OptionType.string, required=True, choices=[
                'Pickups',
            ]),
            discord.Option(name='role', type=discord.OptionType.role, required=True)
        ]
    )
    async def role__set(self, interaction: discord.ApplicationCommandInteraction, section: Literal['Pickups'], role: discord.Role):
        await interaction.response.defer(with_message=True, ephemeral=True)
        if not(interaction.author.guild_permissions.administrator):
            await interaction.send('You do not have permission to use this command.')
        elif role.position >= interaction.author.top_role.position:
            await interaction.send('You cannot use this role due to role hierachy.')
        else:
            await shared.database.set_server_settings('Role', interaction.guild, section, role.id)
            embed = discord.Embed(
                title = 'Role Set',
                description = 'You have successfully set the `{}` Role to {}'.format(section, role.mention),
                colour = role.color,
                timestamp = datetime.now()
            )
            embed.set_author(name='{} • Role Management'.format(interaction.guild.name), icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url)

            await interaction.send(embed=embed)

    # Channel Management

    @commands.slash_command()
    async def channel(self, interaction: discord.ApplicationCommandInteraction):
        ...

    @channel.sub_command(
        name = 'set',
        options = [
            discord.Option(name='section', type=discord.OptionType.string, required=True, choices=[
                'Transactions',
                'Pickups',
                'Logs'
            ]),
            discord.Option(name='channel', type=discord.OptionType.channel, required=True)
        ]
    )
    async def channel__set(self, interaction: discord.ApplicationCommandInteraction, section: Literal['Transactions', 'Pickups', 'Logs'], channel: discord.abc.GuildChannel):
        await interaction.response.defer(with_message=True, ephemeral=True)
        if not(interaction.author.guild_permissions.administrator):
            await interaction.send('You do not have permission to use this command.')
        else:
            await shared.database.set_server_settings('Channel', interaction.guild, section, channel.id)
            embed = discord.Embed(
                title = 'Channel Set',
                description = 'You have successfully set the `{}` Channel to {}'.format(section, channel.mention),
                colour = interaction.author.color,
                timestamp = datetime.now()
            )
            embed.set_author(name='{} • Channel Management'.format(interaction.guild.name), icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url)

            await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(Settings(bot))