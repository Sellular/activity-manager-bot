import discord
from discord.ext import commands

from datetime import datetime, timezone


class OnInteractionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.user:
            self.bot.activeUsersCache[f'{interaction.user.id}'] = datetime.now(
                timezone.utc)


def setup(bot):
    bot.add_cog(OnInteractionCog(bot))
