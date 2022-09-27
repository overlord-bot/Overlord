# Basic Chat Response
import random 
from discord.ext import commands


class AndyChat(commands.Cog, name="Andy Chat"):
    """Andy Chatbot Functions"""

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(AndyChat(bot))
