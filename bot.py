import discord
from discord.ext import commands

from utils import SetupUtils, GeneralUtils, DBUtils


class MyClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=('!'), intents=intents)

    async def on_ready(self):
        print("Bot running with:")
        print("Username: ", self.user.name)
        print("User ID: ", self.user.id)
        print('-----')
        await SetupUtils.resetViews(self)


try:
    DBUtils.checkTables()

    bot = MyClient()
    SetupUtils.importCache(bot)
    SetupUtils.importCogs(bot)
    botConfig = GeneralUtils.getConfig('bot')

    if not botConfig:
        raise Exception("Bot config not found.")

    bot_token = botConfig['token']
    if not bot_token:
        raise Exception("TOKEN not found in Bot config")

    bot.run(bot_token)

except (Exception) as error:
    print(error)
