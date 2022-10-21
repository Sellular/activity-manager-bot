import discord
from discord import NotFound
from discord.ext import commands

from datetime import datetime, timezone

from dao import ChannelMessageDAO
from utils import GeneralUtils
from views.ActiveButtonView import ActiveButtonView


async def getChannelMessage(messageCode: str, channel: discord.TextChannel, bot: commands.Bot):
    message = None
    try:
        channelMessage = ChannelMessageDAO.getChannelMessageByCode(messageCode)
        if channelMessage:
            message = await channel.fetch_message(int(channelMessage.messageID))
        else:
            ChannelMessageDAO.deleteChannelMessageByCode(messageCode)
    except NotFound as error:
        ChannelMessageDAO.deleteChannelMessageByCode(messageCode)
    except Exception as error:
        print(error)
    finally:
        return message


def updateActiveUserTimestamp(bot: commands.Bot, member: discord.Member):
    if member and not member.bot:
        bot.activeUsersCache[f'{member.id}'] = datetime.now(timezone.utc)


async def updateInactiveMessage(bot: commands.Bot):
    try:
        guildConfig = GeneralUtils.getConfig('guild')
        if not guildConfig:
            raise Exception("Guild config not found.")

        inactiveChannelId = guildConfig['inactive_channel_id']
        if not inactiveChannelId:
            raise Exception("INACTIVE_CHANNEL_ID not found in Guild config.")

        inactiveChannel = discord.utils.get(
            bot.get_all_channels(), id=int(inactiveChannelId))

        inactiveEmbed = discord.Embed(title="You're inactive!", description="It appears that you have not been active within our community in the last week." +
                                "\n\n" +
                                "If you are seeing this channel, this means you are at risk of being purged from the community. If you would like to avoid this, hit the button below to be marked active again!")

        inactiveMessage = await getChannelMessage("inactiveMessage", inactiveChannel, bot)

        if inactiveMessage:
            await inactiveMessage.edit(embed=inactiveEmbed, view=ActiveButtonView())
        else:
            inactiveMessage = await inactiveChannel.send(embed=inactiveEmbed, view=ActiveButtonView())
            ChannelMessageDAO.insert(inactiveMessage.id, "inactiveMessage")
    except Exception as error:
        print(error)
