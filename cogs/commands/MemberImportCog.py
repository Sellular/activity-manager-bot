import discord
from discord.ext import commands

from datetime import datetime, timezone

from dao import UserActivityDAO

class MemberImportCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='memberimport', description='Import missing members into activity database', guild_ids=[839673797066096660])
    @commands.has_permissions(administrator=True)
    async def memberImport(self, ctx: discord.ApplicationContext):
        activity_timestamp_ids = [
            (str(member.id), datetime.now(timezone.utc)) for member in ctx.guild.members]

        UserActivityDAO.insertMany(activity_timestamp_ids)
        await ctx.response.send_message("Members imported", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(MemberImportCog(bot))