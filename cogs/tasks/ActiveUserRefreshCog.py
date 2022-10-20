import discord
from discord.ext import tasks, commands

from dao import UserActivityDAO, IgnoredRoleDAO
from utils import GeneralUtils

from datetime import datetime, timedelta, timezone


class ActiveUserRefreshCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.activeUserRefresh.start()

    def cog_unload(self):
        self.activeUserRefresh.cancel()

    @tasks.loop(hours=1)
    async def activeUserRefresh(self):
        bot = self.bot
        try:
            guildConfig = GeneralUtils.getConfig('guild')
            inactiveRoleID = guildConfig['inactive_role_id']
            guildID = guildConfig['guild_id']

            guild = discord.utils.get(bot.guilds, id=int(guildID))
            inactiveRole = discord.utils.get(
                guild.roles, id=int(inactiveRoleID))

            ignoredRoles = IgnoredRoleDAO.getIgnoredRoles()
            ignoredMembers = [member.id for member in [mem for mem in [
                discord.utils.get(guild.roles, id=roleID).members for roleID in ignoredRoles]]]

            activity_timestamp_ids = [
                (memberIDString, bot.activeUsersCache[f'{memberIDString}']) for memberIDString in bot.activeUsersCache.keys()]
            UserActivityDAO.upsertMany(activity_timestamp_ids)

            activeActivities = UserActivityDAO.getUserActivityByActive(True)
            now = datetime.now(timezone.utc)
            twoWeeksAgo = now - timedelta(days=14)
            inactive_id_list = []
            for activity in activeActivities:
                if activity.activeTimestamp < twoWeeksAgo:
                    member = discord.utils.get(
                        guild.members, id=int(activity.memberID))
                    if not member.bot and member.id not in ignoredMembers:
                        await member.remove_roles(member.roles)
                        await member.add_roles(inactiveRole)
                        inactive_id_list.append((activity.memberID,))
                        bot.activeUsersCache.pop(activity.memberID)

            if inactive_id_list:
                UserActivityDAO.userActivitySetManyInactive(inactive_id_list)
        except Exception as error:
            print(error)

    @activeUserRefresh.before_loop
    async def before_userdump(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(ActiveUserRefreshCog(bot))
