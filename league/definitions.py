import discord
import typing

class Team:
    def __init__(self, team: discord.Role, emoji: typing.Optional[discord.Emoji] = None):
        self.team = team
        self.emoji = emoji

    @property
    def server_format(self) -> str:
        return f"{self.emoji} {self.team.mention}" if self.emoji else self.team.mention

    @property
    def display_format(self) -> str:
        return f"{self.emoji} **{self.team.name}**" if self.emoji else self.team.name