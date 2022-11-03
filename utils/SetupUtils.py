import os
from discord.ext import commands

from utils import DiscordUtils
from dao import UserActivityDAO, IgnoredRoleDAO


def importCogs(bot: commands.Bot):
    for filename in os.listdir("./cogs/commands"):
        if filename.endswith(".py"):
            cogName = filename[:-3]
            bot.load_extension("cogs.commands." + cogName)

    for filename in os.listdir("./cogs/events"):
        if filename.endswith(".py"):
            cogName = filename[:-3]
            bot.load_extension("cogs.events." + cogName)

    for filename in os.listdir("./cogs/tasks"):
        if filename.endswith(".py"):
            cogName = filename[:-3]
            bot.load_extension("cogs.tasks." + cogName)


async def resetViews(bot: commands.Bot):
    await DiscordUtils.updateInactiveMessage(bot)


def importCache(bot: commands.Bot):
    bot.activeUsersCache = {}
    activeUsers = UserActivityDAO.getUserActivityByActive(True)
    for activity in activeUsers:
        bot.activeUsersCache[f'{activity.memberID}'] = activity.activeTimestamp
    bot.ignoredRoles = IgnoredRoleDAO.getIgnoredRoles()
