import discord
from discord.ext import commands

from utils import DiscordUtils


class OnApplicationCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command(self, context: discord.ApplicationContext):
        DiscordUtils.updateActiveUserTimestamp(self, context.author)


def setup(bot):
    bot.add_cog(OnApplicationCommandCog(bot))
