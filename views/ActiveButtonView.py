import discord
from discord.ui import View

from utils import GeneralUtils

import asyncio

class ActiveButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Make me active!", style=discord.ButtonStyle.green, custom_id='active_button', emoji="✅")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, invisible=False)
        await asyncio.sleep(0.2) # Thinking...

        guildConfig = GeneralUtils.getConfig('guild')
        inactiveRoleID = guildConfig['inactive_role_id']
        inactiveRole = discord.utils.get(
            interaction.guild.roles, id=int(inactiveRoleID))
        await interaction.user.remove_roles(inactiveRole)
        await interaction.followup.send("You have been made active!", ephemeral=True)
