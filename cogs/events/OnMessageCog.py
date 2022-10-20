import discord
from discord.ext import commands

from utils import DiscordUtils


class OnMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        DiscordUtils.updateActiveUserTimestamp(self, message.author)


def setup(bot):
    bot.add_cog(OnMessageCog(bot))
