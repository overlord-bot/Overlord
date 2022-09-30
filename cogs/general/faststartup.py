# Startup Operations

import os
import platform

import discord
from discord.ext import commands


class Startup(commands.Cog, name="Start Up"):
    """Startup Operations"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("\n---------------------- Connected to Discord --------------------------")
        print(f"{self.bot.user} (ID: {self.bot.user.id}) has connected to Discord!")
        print("----------------------------------------------------------------------")


async def setup(bot):
    await bot.add_cog(Startup(bot))
