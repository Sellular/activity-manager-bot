import discord
from discord.ext import commands

from datetime import datetime, timezone

from dao import UserActivityDAO
from utils import GeneralUtils


class MemberImportCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='memberimport', description='Import missing members into activity database', guild_ids=[int(GeneralUtils.getConfig('guild')['guild_id'])])
    @commands.has_permissions(administrator=True)
    async def memberImport(self, ctx: discord.ApplicationContext):
        await MemberImportCog.memberImportFunction(ctx.guild)
        
        await ctx.response.send_message("Members imported", ephemeral=True)

    async def memberImportFunction(guild):
        activity_timestamp_ids = [
            (str(member.id), datetime.now(timezone.utc)) for member in guild.members]

        UserActivityDAO.insertMany(activity_timestamp_ids)


def setup(bot: commands.Bot):
    bot.add_cog(MemberImportCog(bot))
