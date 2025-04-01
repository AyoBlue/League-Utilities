from disnake.ext import commands
import disnake as discord
import math

decline = {
    'color': 0xFF6161
}
accept = {
    'color': 0x61FF66
}
elo = {
    'up': '<:up:1310002138621018243>',
    'down': '<:down:1310002148901261372>',
    'equal': '<:equal:1310003627880087696>'
}

def probability(rating1: int, rating2: int):
    return 1.0 / (1 + math.pow(10, (rating1 - rating2) / 400.0))

def elo_rating(rating1, rating2, winner):
    rating1 = rating1 + (30 if rating1 < 2000 else 10) * (winner - probability(rating2, rating1))
    rating2 = rating2 + (30 if rating2 < 2000 else 10) * ((1 - winner) - probability(rating1, rating2))
    
    return round(rating1), round(rating2)

def clamp(X: int, Min: int, Max: int):
    return max(Min, min(X, Max))

def normalize(X: int, Min: int, Max: int):
    return ((clamp(X, Min, Max) - Min) / (Max - Min))

def has_premium(bot: commands.InteractionBot, member: discord.Member) -> None:
    guild = bot.get_guild(0) # Set to Support Server ID
    member = discord.utils.get(guild.members, id=member.id)
    if not(member):
        return False
    elif member.id == guild.owner_id:
        return True
    else:
        role = discord.utils.get(member.roles, id=1307591780988092496)
        if role:
            return True
        
def get_emoji(emojis: list[dict], emoji_name: str = None, emoji_id: int = None):
    if emoji_name:
        for emoji in emojis:
            if emoji['name'] == emoji_name:
                return to_emoji(emoji)
    else:
        for emoji in emojis:
            if emoji['id'] == emoji_id:
                return to_emoji(emoji)
        
def to_emoji(emoji): # Used for Bot Emojis since disnake doesn't support it.
    return '<:{}:{}>'.format(emoji['name'], emoji['id'])