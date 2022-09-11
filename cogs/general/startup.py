# Startup Operations

import os
import platform

import discord
from discord.ext import commands


class Startup(commands.Cog, name="Startup"):
    """Startup Operations"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("\n---------------------- Connecting to Discord ------------------------")
        print(f"{self.bot.user} (ID: {self.bot.user.id}) has connected to Discord!")
        print(f"discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print("----------------------------------------------------------------------")


async def setup(bot):
    await bot.add_cog(Startup(bot))
