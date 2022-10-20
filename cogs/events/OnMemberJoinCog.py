import discord
from discord.ext import commands

from utils import DiscordUtils


class OnMemberJoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        DiscordUtils.updateActiveUserTimestamp(self.bot, member)

def setup(bot):
    bot.add_cog(OnMessageCog(bot))
