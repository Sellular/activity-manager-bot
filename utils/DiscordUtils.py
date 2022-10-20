import discord
from discord.ext import commands

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
    except Exception as error:
        print(error)
    finally:
        return message

def updateActiveUserTimestamp(member: discord.Member):
    True

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

        inactiveEmbed = discord.Embed(title="\u200b")
        inactiveEmbed.add_field(name="You're inactive!", value="It appears that you have not been active within our community in the last week." +
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
