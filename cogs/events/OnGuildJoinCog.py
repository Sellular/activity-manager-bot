import discord
from discord.ext import commands

class OnGuildJoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        

def setup(bot):
    bot.add_cog(OnGuildJoinCog(bot))