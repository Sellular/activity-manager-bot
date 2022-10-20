import discord
from discord.ui import View

from utils import GeneralUtils


class ActiveButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Make me active!", style=discord.ButtonStyle.green, custom_id='active_button', emoji="✅")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        guildConfig = GeneralUtils.getConfig('guild')
        inactiveRoleID = guildConfig['inactive_role_id']
        inactiveRole = discord.utils.get(
            interaction.guild.roles, id=int(inactiveRoleID))
        await interaction.user.remove_roles(inactiveRole)
