from typing import Literal, Union
from disnake.ext import commands
from datetime import datetime
import disnake as discord
import shared

class Pickups(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.ranks = ['Silver', 'Gold', 'Platinum', 'Diamond']

    @commands.slash_command(
        description = 'Create a pickup!',
        options = [
            discord.Option(name='gametype', type=discord.OptionType.string, required=True, choices=[
                'Casual',
                'Ranked'
            ]),
            discord.Option(name='member', type=discord.OptionType.user, required=True),
            discord.Option(name='url', type=discord.OptionType.string, required=True)
        ]
    )
    async def pickup(self, interaction: discord.ApplicationCommandInteraction, gametype: Literal['Casual', 'Ranked'], member: Union[discord.Member, discord.User], url: str):
        await interaction.response.defer(with_message=True, ephemeral=True)

        role_settings = await shared.database.get_server_settings('Role', interaction.guild)
        role = discord.utils.get(interaction.guild.roles, id=role_settings.pickups)
        if not(discord.utils.get(interaction.author.roles, id=role_settings.pickups)) and not(interaction.guild.owner_id == interaction.author.id):
            await interaction.send('You are not allowed to use this command.')
        elif member == interaction.author.id:
            await interaction.send('You cannot do a pickup with yourself...')
        elif not(discord.utils.get(member.roles, id=role_settings.pickups)):
            await interaction.send('The player you\'re challenging does not have {}'.format(role.mention if role else 'the required Pickup Role.'))
        else:
            if gametype == 'Casual':
                ...
            else:
                if (await shared.database.search('SELECT * FROM RankedQBBs WHERE Player1=$1 OR Player2=$1', interaction.author.id)):
                    await interaction.send('You are currently in the middle of a Ranked QBB.'.format(interaction.author.mention, interaction.author))
                elif (await shared.database.search('SELECT * FROM RankedQBBs WHERE Player1=$1 OR Player2=$1', member.id)):
                    await interaction.send('{} `{}` is currently in the middle of a Ranked QBB.'.format(member.mention, member))
                else:
                    client_qbb = await shared.database.get_player('QBB', interaction.guild, interaction.author, True)
                    target_qbb = await shared.database.get_player('QBB', interaction.guild, member, True)

                    embed = discord.Embed(
                        title = 'Ranked QBB',
                        description = '{} `{}` has challenged {} `{}` to a Ranked QBB!'.format(
                            interaction.author.mention,
                            interaction.author,
                            member.mention,
                            member
                        ),
                        colour = client_qbb.rank.color,
                        timestamp = datetime.now()
                    )
                    embed.set_footer(text=interaction.author, icon_url=interaction.author.display_avatar.url if interaction.author.display_avatar else None)
                    embed.set_author(name=f'{interaction.guild.name} • Pickups', icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

                    embed.add_field(name='Player 1', value='''{} `{}`
{} **{}** ({} / {})
{} Wins / {} Losses
{} Games / {}% Win Rate'''.format(
                        interaction.author.mention,
                        interaction.author,
                        f'<:{client_qbb.rank.name}:{client_qbb.rank.emoji_id}>',
                        client_qbb.rank.name,
                        client_qbb.elo,
                        client_qbb.peak_elo,

                        client_qbb.wins,
                        client_qbb.losses,
                        client_qbb.wins + client_qbb.losses,
                        '0.00' if (client_qbb.wins + client_qbb.losses == 0) else '{:.2f}'.format(shared.utils.normalize(client_qbb.wins, 0, client_qbb.wins + client_qbb.losses) * 100)
                    ), inline=True)

                    embed.add_field(name='Player 2', value='''{} `{}`
{} **{}** ({} / {})
{} Wins / {} Losses
{} Games / {}% Win Rate'''.format(
                        member.mention,
                        member,
                        f'<:{target_qbb.rank.name}:{target_qbb.rank.emoji_id}>',
                        target_qbb.rank.name,
                        target_qbb.elo,
                        target_qbb.peak_elo,

                        target_qbb.wins,
                        target_qbb.losses,
                        target_qbb.wins + target_qbb.losses,
                        '0.00' if (target_qbb.wins + target_qbb.losses == 0) else '{:.2f}'.format(shared.utils.normalize(target_qbb.wins, 0, target_qbb.wins + target_qbb.losses) * 100)
                    ), inline=True)

                    channel_settings = await shared.database.get_server_settings('Channel', interaction.guild)
                    components = discord.ui.ActionRow()
                    components.add_button(
                        style = discord.ButtonStyle.green,
                        label = 'Report Score',
                        custom_id = 'Report',
                        emoji = '📋'
                    )
                    channel = discord.utils.get(interaction.guild.channels, id=channel_settings.pickups) or interaction.channel
                    message = await channel.send(embed=embed, components=[
                        components,
                        discord.ui.Button(
                            style = discord.ButtonStyle.url,
                            label = 'Play',
                            emoji = '🏈',
                            url = url
                        )
                    ])
                    await shared.database.create_qbb(interaction.guild, interaction.author, member, message)
                    await interaction.send('A `{}` Pickup successfully created!'.format(gametype))

def setup(bot):
    bot.add_cog(Pickups(bot))