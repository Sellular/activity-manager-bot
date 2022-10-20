import discord
from discord.ext import commands

from datetime import datetime, timezone


class OnReactionRemoveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, member: discord.Member):
        if member:
            self.bot.activeUsersCache[f'{member.id}'] = datetime.now(
                timezone.utc)


def setup(bot):
    bot.add_cog(OnReactionRemoveCog(bot))
