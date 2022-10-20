import discord
from discord.ext import commands

from datetime import datetime, timezone

class OnVoiceStateUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member:
            self.bot.activeUsersCache[f'{member.id}'] = datetime.now(timezone.utc)
    

def setup(bot):
    bot.add_cog(OnVoiceStateUpdateCog(bot))