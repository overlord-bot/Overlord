# Common Events

from discord.ext import commands


class CommonEvents(commands.Cog, name="Common Events"):
    """Common Server Events"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            welcome_msg = f"Welcome {member.mention} to {guild.name}!"
            await guild.system_channel.send(welcome_msg)


async def setup(bot):
    await bot.add_cog(CommonEvents(bot))
