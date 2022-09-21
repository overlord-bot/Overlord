# Startup Operations

import os
import platform

import discord
from discord.ext import commands

# If you are not planning on developing application or slash commands ignore this.
# FOR MAIN RELEASE CHANGE testing_server TO NONE OR FALSE
testing_server = discord.Object(id=333409598365106176)
#                                 ^^^^^^^^^^^^^^^^^^
#                               Insert your server id here
#                         (make sure discord dev mode is enabled)
# Click "Copy Id": https://i.gyazo.com/3499ab2ba0219b07e7e892355931c17a.png

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
        if (testing_server):
            self.bot.tree.copy_global_to(guild=testing_server)
            await self.bot.tree.sync(guild=testing_server)
            print(f"Syncing commands to server id: {testing_server.id}")
        else:
            print("Syncing commands globally")
            await self.bot.tree.sync()
        print("----------------------------------------------------------------------")


async def setup(bot):
    await bot.add_cog(Startup(bot))
