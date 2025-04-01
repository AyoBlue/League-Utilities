from datetime import datetime, timedelta
from typing import Literal, Union
from disnake.ext import commands
import disnake as discord
from . import types
import asyncpg
import asyncio
import os

# Anything Database related is done here.
connection: asyncpg.Connection = None

async def create_connection(loop: asyncio.AbstractEventLoop = None):
    global connection
    connection = await asyncpg.connect(
        user = 'ayoblue',
        password = os.environ['PASSWD'],
        database = 'League Utilities',
        host = os.environ['HOST'],
        timeout = 10,
        loop = loop
    )

async def search(statement: str, *args):
    return await connection.fetch(statement, *args)

async def get_teams(server: discord.Guild) -> list[asyncpg.Record]:
    results = await connection.fetch('SELECT * FROM Teams WHERE Guild=$1', server.id)
    return results

async def get_team(server: discord.Guild, role: discord.Role) -> None:
    team = await connection.fetchrow('SELECT * FROM Teams WHERE Role=$1 AND Guild=$2', role.id, server.id)
    return team or None

async def get_coach(server: discord.Guild, role: discord.Role) -> None:
    coach = await connection.fetchrow('SELECT * FROM CoachRoles WHERE Role=$1 AND Guild=$2', role.id, server.id)
    return coach or None

async def add_team(server: discord.Guild, team: discord.Role, emoji: discord.Emoji = None) -> Literal['Max', 'Exists', True]:
    teams = await get_teams(server)
    if len(teams) >= 128:
        return 'Max'
    
    if (await get_team(server, team)):
        return 'Exists'
    
    emoji_id: int = emoji.id if isinstance(emoji, discord.Emoji) else 0
    await connection.execute('INSERT INTO Teams VALUES($1, $2, $3)', server.id, team.id, emoji_id)
    return True

async def add_coach(server: discord.Guild, role: discord.Role, limit: int = 1):
    coach = await get_coach(server, role)
    if coach:
        return 'Exists'
    
    await connection.execute('INSERT INTO CoachRoles VALUES($1, $2, $3)', server.id, role.id, limit)
    return True

async def remove_team(server: discord.Guild, team: discord.Role):
    await connection.execute('DELETE FROM Teams WHERE Guild=$1 AND Role=$2', server.id, team.id)

async def remove_coach(server: discord.Guild, role: discord.Role):
    await connection.execute('DELETE FROM CoachRoles WHERE Guild=$1 AND Role=$2', server.id, role.id)

async def get_server_settings(section: Literal['Channel', 'Role'], server: discord.Guild):
    data = await connection.fetchrow('SELECT * FROM Guild{}Settings WHERE Guild=$1'.format(section), server.id)
    if not(data):
        await connection.execute('INSERT INTO Guild{}Settings VALUES($1)'.format(section), server.id)
        data = await connection.fetchrow('SELECT * FROM Guild{}Settings WHERE Guild=$1'.format(section), server.id)

    data = list(data.values())
    if section == 'Channel':
        return types.GuildChannelSettings(data)
    elif section == 'Role':
        return types.GuildRoleSettings(data)
    else:
        ...

async def set_server_settings(section: Literal['Channel', 'Role', 'Guild'], server: discord.Guild, key: str, value: Union[int, str]):
    await get_server_settings(section, server)
    await connection.execute('UPDATE Guild{}Settings SET {}=$1 WHERE Guild=$2'.format(section, key), value, server.id)

async def get_player(section: Literal['League', 'QBB'], server: discord.Guild, member: Union[discord.Member, int], create_account: bool = False):
    if section == 'QBB':
        user_id: int = member.id if isinstance(member, discord.Member) else member
        data = await connection.fetchrow('SELECT * FROM QBBPlayers WHERE Member=$1', user_id)
        if not(data):
            if create_account:
                await connection.execute('INSERT INTO QBBPlayers VALUES($1, $2, $3)', server.id, user_id, 1)
                data = await connection.fetchrow('SELECT * FROM QBBPlayers WHERE Guild=$1 AND Member=$2', server.id, user_id)
            else:
                data = {
                    'elo': 0,
                    'peak_elo': 0,
                    'wins': 0,
                    'losses': 0,
                    'rank': 'Unranked'
                }

        leaderboard = await connection.fetch(
            '''
            SELECT
                *
            FROM
                QBBPlayers
            WHERE
                Guild=$1
            ORDER BY
                Elo
            DESC
            FETCH FIRST 3 ROW ONLY;
            ''', server.id
        )
        if not(isinstance(data, dict)):
            data = {
                'elo': data[3],
                'peak_elo': data[4],
                'wins': data[5],
                'losses': data[6]
            }
            if (data['elo'] > 2000) and len(list(filter(lambda x: x.member == user_id, leaderboard))) > 0:
                data['rank'] = types.ranks[-1]['rank']
            else:
                for rank in types.ranks:
                    if (data['elo'] >= rank['elo'][0]) and data['elo'] < rank['elo'][1]:
                        data['rank'] = rank['rank']
                        break

        return types.QBBPlayer(**data)
    elif section == 'League':
        teams = await get_teams(server)
        data = {}
        for record in teams:
            if len(data.keys()) > 2:
                break

            if not(data.get('role')):
                team = discord.utils.get(member.roles, id=record.get('role'))
                if team:
                    data['role'] = team
                    data['emoji'] = discord.utils.get(member.guild.emojis, id=record.get('emoji'))

                    continue
            
            if not(data.get('coach')):
                try:
                    ...
                except:
                    ...
                else:
                    ...

        data['member'] = member
        return types.LeaguePlayer(**data)
    else:
        ...

async def create_qbb(
    server: discord.Guild,
    player1: discord.Member,
    player2: discord.Member,
    message: discord.Message
):
    timestamp = datetime.now() + timedelta(hours=1.5)
    await connection.execute(
        'INSERT INTO RankedQBBs VALUES($1, $2, $3, $4, $5)',
        server.id,
        player1.id,
        player2.id,
        message.id,
        timestamp.strftime('%d/%m/%Y, %H:%M:%S')
    )

async def get_qbb(
    message: discord.Message = None,
    players: list[discord.Member] = []
) -> types.QBB:
    if len(players) > 1:
        qbb = await connection.fetchrow('''
            SELECT
                *
            FROM 
                RankedQBBs
            WHERE
                (Player1=$1 AND Player2=$2)
            OR
                (Player1=$2 AND Player2=$1)
        ''', *players)
        if (qbb):
            return types.QBB(qbb)
    elif message:
        qbb = await connection.fetchrow('SELECT * FROM RankedQBBs WHERE Message=$1', message.id)
        if qbb:
            return types.QBB(qbb)
        
async def update_qbb_score(
    server: discord.Guild,
    message: discord.Message,
    player: Literal['Player1', 'Player2'],
    score: str
) -> True:
    qbb = await get_qbb(message)
    if not(qbb):
        return None
    else:
        await connection.execute('UPDATE RankedQBBs SET {}Report=$1 WHERE (Message=$2 AND Guild=$3)'.format(
            player
        ), score, message.id, server.id)
        return True
    
async def set_elo(
    server: discord.Guild,
    member: Union[discord.Member, int],
    rating: int,
    won: bool
):
    user_id: int = member.id if isinstance(member, discord.Member) else member
    qbb = await get_player('QBB', server, member, True)
    if won:
        qbb.wins += 1
    elif won == False:
        qbb.losses += 1

    await connection.execute('UPDATE QBBPlayers SET Elo=$1, Wins=$2, Losses=$3 WHERE Member=$4', rating, qbb.wins, qbb.losses, user_id)

async def remove_qbb(
    server: discord.Guild,
    message: discord.Message
):
    await connection.execute('DELETE FROM RankedQBBs WHERE Guild=$1 AND Message=$2', server.id, message.id)