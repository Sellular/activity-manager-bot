import discord
from discord.ext import commands

from utils import DiscordUtils


class OnVoiceStateUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        DiscordUtils.updateActiveUserTimestamp(self.bot, member)


def setup(bot):
    bot.add_cog(OnVoiceStateUpdateCog(bot))
