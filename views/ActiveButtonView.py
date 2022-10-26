import discord
from discord.ui import View

from utils import GeneralUtils
from dao import LeftMemberRoleDAO

import asyncio

class ActiveButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Make me active!", style=discord.ButtonStyle.green, custom_id='active_button', emoji="✅")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, invisible=False)
        await asyncio.sleep(0.2) # Thinking...

        member = interaction.user
        guildConfig = GeneralUtils.getConfig('guild')
        inactiveRoleID = guildConfig['inactive_role_id']
        inactiveRole = discord.utils.get(
            interaction.guild.roles, id=int(inactiveRoleID))
        await interaction.user.remove_roles(inactiveRole)

        inactiveMemberRoles = LeftMemberRoleDAO.getLeftMemberRolesByMember(str(member.id))
        LeftMemberRoleDAO.deleteLeftMemberRolesByMember(str(member.id))

        if inactiveMemberRoles:
            guild = member.guild
            for role in inactiveMemberRoles:
                guild_role = discord.utils.get(guild.roles, id=int(role.roleID))
                await member.add_roles(guild_role)

        await interaction.followup.send("You have been made active!", ephemeral=True)
