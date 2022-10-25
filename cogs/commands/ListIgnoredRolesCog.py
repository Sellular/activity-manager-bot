from discord import slash_command, option, Interaction
from discord.ext import commands
from discord.utils import get

from dao import IgnoredRoleDAO
from utils import GeneralUtils


class ListIgnoredRolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name='listignoredroles', guild_ids=[int(GeneralUtils.getConfig('guild')['guild_id'])], description="List ignored roles")
    @commands.has_permissions(administrator=True)
    async def listIgnoredRoles(self, interaction: Interaction):
        ignored_role_ids = IgnoredRoleDAO.getIgnoredRoles()
        ignored_roles = [get(interaction.guild.roles, id=int(ignored_id)) for ignored_id in ignored_role_ids]
        if not ignored_roles:
            roles_string = ', '.join([role.name for role in ignored_roles])
            await interaction.response.send_message(f"Currently ignored roles: {roles_string}", ephemeral=True)
            return

        await interaction.response.send_message("No roles are currently being ignored.", ephemeral=True)
        

def setup(bot: commands.Bot):
    bot.add_cog(ListIgnoredRolesCog(bot))
