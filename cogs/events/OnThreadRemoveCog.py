import discord
from discord.ext import commands

from datetime import datetime, timezone

class OnThreadRemoveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command(self, thread: discord.Thread):
        if thread.owner:
            self.bot.activeUsersCache[f'{thread.owner.id}'] = datetime.now(timezone.utc)
    

def setup(bot):
    bot.add_cog(OnThreadRemoveCog(bot))