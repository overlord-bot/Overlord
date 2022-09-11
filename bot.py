# bot.py

import asyncio
import os

import discord
from discord.ext import commands

from dotenv import load_dotenv  # pip install python-dotenv


intents = discord.Intents.default()
intents.members = True  # permission to see server members
intents.message_content = True  # permission to read message content

bot_status = "With Fate | Try !help "
bot_description = "This is the full help description"
bot = commands.Bot(command_prefix="!", description=bot_description, intents=intents, activity=discord.Game(name=bot_status))


async def load_cogs():
    print("\n------------------ Loading Cogs -----------------")
    for folder in os.listdir("cogs"):
        for filename in os.listdir(os.path.join(f"cogs/{folder}")):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{folder}.{filename[:-3]}")
                    print(f"Success Loading: cogs.{folder}.{filename}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed Loading: cogs.{folder}.{filename} | Error: {exception}")


async def main():
    await load_cogs()

    load_dotenv()
    await bot.start(os.getenv("DISCORD_TOKEN"))  # fetches token from env file stored locally and starts bot

asyncio.run(main())
