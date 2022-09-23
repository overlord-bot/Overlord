# bot.py

import asyncio
import os

import discord
from discord.ext import commands

from dotenv import load_dotenv  # pip install python-dotenv


class Bot(commands.Bot):
    def __init__(self) -> None:
        self.testing_server = None
        load_dotenv()
        self.testing_server = discord.Object(os.getenv("TESTING_SERVER_ID"))

        # Necessary intents (permissions) for the bot to function
        intents = discord.Intents.default()
        intents.members = True  # permission to see server members
        intents.message_content = True  # permission to read message content

        # Set up the bot object and its descriptions
        bot_status = "With Fate | Try !help "
        bot_description = "This is the full help description"
        super().__init__(command_prefix="!", description=bot_description, intents=intents, activity=discord.Game(name=bot_status))

    async def setup_hook(self) -> None:
        await self.load_cogs()

    # Load all cogs inside the cogs folder
    async def load_cogs(self) -> None:
        print("\n------------------ Loading Cogs -----------------")
        for folder in os.listdir("cogs"):
            for filename in os.listdir(os.path.join(f"cogs/{folder}")):
                if filename.endswith(".py"):
                    try:
                        await self.load_extension(f"cogs.{folder}.{filename[:-3]}")
                        print(f"Success Loading: cogs.{folder}.{filename}")
                    except Exception as e:
                        exception = f"{type(e).__name__}: {e}"
                        print(f"Failed Loading: cogs.{folder}.{filename} | Error: {exception}")


bot = Bot()
load_dotenv()
asyncio.run(bot.run(os.getenv("DISCORD_TOKEN")))  # fetches token from env file stored locally and starts bot
