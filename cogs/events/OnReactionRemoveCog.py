import discord
from discord.ext import commands

from utils import DiscordUtils


class OnReactionRemoveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, member: discord.Member):
        DiscordUtils.updateActiveUserTimestamp(self.bot, member)


def setup(bot):
    bot.add_cog(OnReactionRemoveCog(bot))
