from typing import Literal, Union, TypedDict
import disnake as discord
import datetime
import math

Games = Literal['Football Fusion', 'Football Universe', 'Basketball Legends', 'Football Legends']

ranks = [
    {
        'rank': 'Unranked',
        'elo': [-1, -1],
        'color': 0x1F1F1F,
        'emoji': 1309220393067741235
    },
    {
        'rank': 'Rookie',
        'elo': [0, 1250],
        'color': 0xE29A6C,
        'emoji': 1309266044392837120,
    },
    {
        'rank': 'Experienced',
        'elo': [1250, 1500],
        'color': 0xF2F7FB,
        'emoji': 1309220261496754187,
    },
    {
        'rank': 'Adapt',
        'elo': [1500, 1750],
        'color': 0xFDEE9D,
        'emoji': 1309220219956494468,
    },
    {
        'rank': 'Elite',
        'elo': [1750, 2000],
        'color': 0xA8E0FE,
        'emoji': 1309220205632950282,
    },
    {
        'rank': 'Master',
        'elo': [2000, 9999],
        'color': 0xEF8E8E,
        'emoji': 1309220194832355429,
    },
    {
        'rank': 'Grandmaster',
        'color': 0xBB9AF2,
        'emoji': 1309220184661430393,
    },
]

class Rank:
    def __init__(
        self,
        rank: Literal['Rookie', 'Experienced', 'Adapt', 'Elite', 'Master', 'Grandmaster']
    ):
        player_rank = list(filter(lambda x: x['rank'] == rank, ranks))[0]

        self.name = player_rank['rank']
        self.color = player_rank['color']
        self.emoji_id = player_rank['emoji']

class QBBPlayer:
    def __init__(
        self,
        elo: int,
        peak_elo: int,
        wins: int,
        losses: int,
        rank: Literal['Rookie', 'Experienced', 'Adapt', 'Elite', 'Master', 'Grandmaster'],
    ):
        self.elo = elo
        self.peak_elo = peak_elo
        self.wins = wins
        self.losses = losses
        self.rank = Rank(rank)

class QBB:
    def __init__(self, data):
        self.guild = data[0]
        self.player1 = data[1]
        self.player2 = data[2]
        self.message_id = data[3]
        self.timestamp = datetime.datetime.strptime(data[4], '%d/%m/%Y, %H:%M:%S')
        self.player1report = data[5]
        self.player2report = data[6]

class LeaguePlayer:
    def __init__(
        self,
        role: discord.Role = None,
        emoji: discord.Emoji = None,
        coach: discord.Role = None,
        member: discord.Member = None,
    ):
        self.role = role
        self.emoji = emoji
        self.coach = coach
        self.member = member

class GuildChannelSettings:
    def __init__(self, data):
        self.server_id = data[0]
        self.transactions = data[1]
        self.pickups = data[2]

class GuildRoleSettings:
    def __init__(self, data):
        self.server_id = data[0]
        self.pickups = data[1]