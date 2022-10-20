import discord
from discord.ext import commands

from datetime import datetime, timezone

from utils import DiscordUtils

class OnInteractionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        DiscordUtils.updateActiveUserTimestamp(self.bot, interaction.user)


def setup(bot):
    bot.add_cog(OnInteractionCog(bot))
