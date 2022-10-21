from discord import slash_command, option, Interaction, Role
from discord.ext import commands

from dao import IgnoredRoleDAO
from utils import GeneralUtils


class ActivityIgnoreRoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name='activityignorerole', guild_ids=[int(GeneralUtils.getConfig('guild')['guild_id'])], description='Ignore activity of given role')
    @option('role', Role, description='Role to be ignored', required=True)
    @commands.has_permissions(administrator=True)
    async def activityIgnoreRole(self, interaction: Interaction, role: Role):
        if role.id in self.bot.ignoredRoles:
            await interaction.response.send_message("Role is already ignored.", ephemeral=True)
        else:
            IgnoredRoleDAO.insert(role.id)
            await interaction.response.send_message("Role has been ignored.", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(ActivityIgnoreRoleCog(bot))
