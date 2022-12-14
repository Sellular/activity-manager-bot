import discord
from discord.ext import tasks, commands

from dao import UserActivityDAO, IgnoredRoleDAO, LeftMemberRoleDAO
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
        guildConfig = GeneralUtils.getConfig('guild')
        inactiveRoleID = guildConfig['inactive_role_id']
        inactivePingChannelID = guildConfig['inactive_ping_channel_id']
        guildID = guildConfig['guild_id']

        guild = discord.utils.get(bot.guilds, id=int(guildID))
        if not guild:
            print(f"Guild with given id: {guildID} not found.")
            return

        inactiveRole = discord.utils.get(
            guild.roles, id=int(inactiveRoleID))
        if not inactiveRole:
            print(f"Inactive role with given id: {inactiveRoleID} not found.")

        inactivePingChannel = discord.utils.get(
            guild.channels, id=int(inactivePingChannelID))
        if not inactivePingChannel:
            print(f"Inactive ping channel with given id: {inactivePingChannelID} not found.")

        ignoredMembers = [member.id for memberArr in [
                discord.utils.get(guild.roles, id=roleID).members for roleID in bot.ignoredRoles] 
            for member in memberArr]

        activity_timestamp_ids = [
            (memberIDString, bot.activeUsersCache[f'{memberIDString}']) for memberIDString in bot.activeUsersCache.keys()]
        UserActivityDAO.upsertMany(activity_timestamp_ids)

        activeActivities = UserActivityDAO.getUserActivityByActive(True)
        now = datetime.now(timezone.utc)
        twoWeeksAgo = now - timedelta(weeks=2)
        inactive_id_list = []
        for activity in activeActivities:
            if activity.activeTimestamp < twoWeeksAgo:
                member = discord.utils.get(
                    guild.members, id=int(activity.memberID))
                
                if not member:
                    UserActivityDAO.deleteUserActivityByMember(activity.memberID)
                elif not member.bot and member.id not in ignoredMembers:
                    try:
                        inactive_role_list = []
                        for role in member.roles:
                            inactive_id_list.append(
                                (str(member.id), str(role.id), str(now)))
                        LeftMemberRoleDAO.insertMany(inactive_role_list)

                        await member.edit(roles=[])
                        await member.add_roles(inactiveRole)

                        inactivePingMessage = await inactivePingChannel.send(f"<@{member.id}>")
                        await inactivePingMessage.delete()

                        inactive_id_list.append((activity.memberID,))
                    except discord.errors.Forbidden as error:
                        print(f"WARN: User {member.name} id: {member.id} has role higher than bot's highest role. User will not be inactivated.")
                        pass

                try:
                    bot.activeUsersCache.pop(activity.memberID)
                except KeyError as error:
                    pass

        if inactive_id_list:
            UserActivityDAO.userActivitySetManyInactive(inactive_id_list)

    @activeUserRefresh.before_loop
    async def before_userdump(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(ActiveUserRefreshCog(bot))
