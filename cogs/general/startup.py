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
        print("\n---------------------- Connecting to Discord ------------------------")
        print(f"{self.bot.user} (ID: {self.bot.user.id}) has connected to Discord!")
        print(f"discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")

        await self.bot.wait_until_ready()

        # Syncs bot commands with the specific bot testing server in bot.py
        # If a server id is not provided, new commands added may take an hour or more to sync with discord
        if self.bot.testing_server:
            self.bot.tree.copy_global_to(guild=self.bot.testing_server)
            await self.bot.tree.sync(guild=self.bot.testing_server)
            print(f"Syncing commands to server id: {self.bot.testing_server.id}")
        else:
            print("Syncing commands globally")
            await self.bot.tree.sync()
        print("----------------------------------------------------------------------")


async def setup(bot):
    await bot.add_cog(Startup(bot))
