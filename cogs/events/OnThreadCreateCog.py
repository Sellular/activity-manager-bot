import discord
from discord.ext import commands

from utils import DiscordUtils


class OnThreadCreateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        DiscordUtils.updateActiveUserTimestamp(self.bot, thread.owner)


def setup(bot):
    bot.add_cog(OnThreadCreateCog(bot))
