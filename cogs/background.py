from datetime import datetime, timedelta
from disnake.ext import commands
import disnake as discord
import shared

class QBBResponse(discord.ui.Modal):
    def __init__(self, message: discord.Message, player1: discord.Member, player2: discord.Member, player):
        components = [
            discord.ui.TextInput(
                label = '{} Score'.format(player1),
                custom_id = 'Player1',
                placeholder = 'Player 1 Score',
                required = True,
                style = discord.TextInputStyle.short
            ),
            discord.ui.TextInput(
                label = '{} Score'.format(player2),
                custom_id = 'Player2',
                placeholder = 'Player 2 Score',
                required = True,
                style = discord.TextInputStyle.short
            )
        ]

        self.message = message
        self.player = player
        super().__init__(
            title = 'Ranked QBB Review',
            components = components
        )
    
    async def callback(self, interaction: discord.ModalInteraction):
        for _, value in interaction.text_values.items():
            if not(value.isnumeric()):
                return await interaction.send('`{}` is not a valid number.'.format(value), ephemeral=True)
        
        score = '{}-{}'.format(
            int(interaction.text_values['Player1']),
            int(interaction.text_values['Player2'])
        )
        await interaction.response.defer(with_message=True, ephemeral=True)
        await shared.database.update_qbb_score(interaction.guild, self.message, self.player, score)
        
        qbb = await shared.database.get_qbb(self.message)
        if qbb.player1report and qbb.player2report:
            if qbb.player1report == qbb.player2report:
                player1score, player2score = score.split('-')
                player1score, player2score = int(player1score), int(player2score)

                player1 = await shared.database.get_player('QBB', interaction.guild, qbb.player1)
                player2 = await shared.database.get_player('QBB', interaction.guild, qbb.player2)
                rating1: int = None
                rating2: int = None
                if player1score == player2score:
                    rating1, rating2 = player1.elo, player2.elo
                else:
                    rating1, rating2 = shared.utils.elo_rating(player1.elo, player2.elo, 1 if player1score > player2score else 0)
                    await shared.database.set_elo(interaction.guild, qbb.player1, rating1, True if player1score > player2score else False)
                    await shared.database.set_elo(interaction.guild, qbb.player2, rating2, False if player1score > player2score else True)
                    if player1score > player2score:
                        player1.wins += 1
                        player2.losses += 1
                    else:
                        player1.losses += 1
                        player2.wins += 1

                    player1.peak_elo = rating1 if player1.peak_elo < rating1 else player1.peak_elo
                    player2.peak_elo = rating2 if player2.peak_elo < rating2 else player2.peak_elo

                player1member = discord.utils.get(interaction.guild.members, id=qbb.player1)
                player2member = discord.utils.get(interaction.guild.members, id=qbb.player2)
                embed = discord.Embed(
                    title = 'Ranked QBB',
                    description = 'The results are in!\n> 📝 **Score:** {}'.format(score),
                    colour = player1.rank.color,
                    timestamp = datetime.now()
                )
                embed.set_footer(text=player1member, icon_url=player1member.display_avatar.url if player1member.display_avatar else None)
                embed.set_author(name=f'{interaction.guild.name} • Pickups', icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
                
                embed.add_field(name='Player 1', value='''{} `{}`
{} **{}** ({} / {}) {} ({})
{} Wins / {} Losses
{} Games / {}% Win Rate'''.format(
                    player1member.mention,
                    player1member,
                    f'<:{player1.rank.name}:{player1.rank.emoji_id}>',
                    player1.rank.name,
                    rating1,
                    player1.peak_elo,
                    shared.utils.elo['up'] if player1score > player2score else shared.utils.elo['equal'] if player1score == player2score else shared.utils.elo['down'],
                    f'+{rating1 - player1.elo}' if rating1 > player1.elo else '0' if rating1 == player1.elo else f'{rating1 - player2.elo}',

                    player1.wins,
                    player1.losses,
                    player1.wins + player1.losses,
                    '0.00' if (player1.wins + player1.losses == 0) else '{:.2f}'.format(shared.utils.normalize(player1.wins, 0, player1.wins + player1.losses) * 100)
                ), inline=True)

                embed.add_field(name='Player 2', value='''{} `{}`
{} **{}** ({} / {}) {} ({})
{} Wins / {} Losses
{} Games / {}% Win Rate'''.format(
                    player2member.mention,
                    player2member,
                    f'<:{player2.rank.name}:{player2.rank.emoji_id}>',
                    player2.rank.name,
                    rating2,
                    player2.peak_elo,
                    shared.utils.elo['up'] if player2score > player1score else shared.utils.elo['equal'] if player2score == player1score else shared.utils.elo['down'],
                    f'+{rating2 - player2.elo}' if rating2 > player2.elo else '0' if rating2 == player2.elo else f'{rating2 - player2.elo}',

                    player2.wins,
                    player2.losses,
                    player2.wins + player2.losses,
                    '0.00' if (player2.wins + player2.losses == 0) else '{:.2f}'.format(shared.utils.normalize(player2.wins, 0, player2.wins + player2.losses) * 100)
                ), inline=True)
                await self.message.edit(embed=embed, components=None)
                await shared.database.remove_qbb(interaction.guild, self.message)
            else:
                await interaction.send('The scores reported do not match, a report has been made!')
        else:
            await interaction.send('You have reported the score as `{}`'.format(score))

class Background(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await shared.database.create_connection()

    @commands.Cog.listener()
    async def on_button_click(self, interaction: discord.MessageInteraction):
        ranked_qbb = await shared.database.get_qbb(interaction.message)
        if (ranked_qbb) and interaction.data.custom_id == 'Report':
            if not(interaction.author.id == ranked_qbb.player1) and not(interaction.author.id == ranked_qbb.player2):
                return await interaction.response.defer()

            player1 = discord.utils.get(interaction.guild.members, id=ranked_qbb.player1) if not(interaction.author.id == ranked_qbb.player1) else interaction.author
            player2 = discord.utils.get(interaction.guild.members, id=ranked_qbb.player2) if not(interaction.author.id == ranked_qbb.player2) else interaction.author
            await interaction.response.send_modal(
                QBBResponse(
                    interaction.message,
                    player1,
                    player2,
                    'Player1' if player1.id == interaction.author.id else 'Player2'
                )
            )


def setup(bot):
    bot.add_cog(Background(bot))