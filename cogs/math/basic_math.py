# Basic Math Operations

from discord.ext import commands


class BasicMath(commands.Cog, name="BasicMath"):
    """Calculates basic math"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, context, left: int, right: int):
        """Adds two numbers together."""  # this is the description that will show up in !help
        await context.send(left + right)


async def setup(bot):
    await bot.add_cog(BasicMath(bot))
