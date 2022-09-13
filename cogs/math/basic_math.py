# Basic Math Operations

from discord.ext import commands


class BasicMath(commands.Cog, name="Basic Math"):
    """Calculates basic math"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, context, left: int, right: int):
        """Adds two numbers"""  # this is the description that will show up in !help
        await context.send(left + right)

    @commands.command()
    async def subtract(self, context, left: int, right: int):
        """Subtracts first number from the second"""  # this is the description that will show up in !help
        await context.send(left - right)


async def setup(bot):
    await bot.add_cog(BasicMath(bot))
