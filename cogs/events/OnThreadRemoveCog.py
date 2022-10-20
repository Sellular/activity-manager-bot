import discord
from discord.ext import commands

from utils import DiscordUtils


class OnThreadRemoveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command(self, thread: discord.Thread):
        DiscordUtils.updateActiveUserTimestamp(self, thread.owner)


def setup(bot):
    bot.add_cog(OnThreadRemoveCog(bot))
