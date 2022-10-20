import discord
from discord.ext import commands

from datetime import datetime, timezone


class OnMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author:
            self.bot.activeUsersCache[f'{message.author.id}'] = datetime.now(
                timezone.utc)


def setup(bot):
    bot.add_cog(OnMessageCog(bot))
