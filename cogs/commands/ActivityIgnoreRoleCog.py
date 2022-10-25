from discord import slash_command, option, Interaction, Role
from discord.ext import commands

from dao import IgnoredRoleDAO
from utils import GeneralUtils


class ActivityIgnoreRoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name='activityignorerole', guild_ids=[int(GeneralUtils.getConfig('guild')['guild_id'])], description='Ignore activity of given role')
    @option('role0', Role, description='Role to be ignored', required=True)
    @option('role1', Role, description="Next role to be ignored", required=False)
    @option('role2', Role, description="Third role to be ignored", required=False)
    @commands.has_permissions(administrator=True)
    async def activityIgnoreRole(self, interaction: Interaction, role0: Role, role1: Role, role2: Role):
        roles = [role0, role1, role2]
        for role in roles:
            if role:
                if role.id in self.bot.ignoredRoles:
                    await interaction.response.send_message(f"Role {role.name} is already ignored.", ephemeral=True)
                else:
                    IgnoredRoleDAO.insert(role.id)
                    await interaction.response.send_message(f"Role {role.name} has been ignored.", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(ActivityIgnoreRoleCog(bot))
