import discord
from discord.ext import commands

from datetime import datetime, timezone


class OnApplicationCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command(self, context: discord.ApplicationContext):
        if context.author:
            self.bot.activeUsersCache[f'{context.author.id}'] = datetime.now(
                timezone.utc)


def setup(bot):
    bot.add_cog(OnApplicationCommandCog(bot))
