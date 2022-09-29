# bot.py

import asyncio
import os

import discord
from discord.ext import commands

from dotenv import load_dotenv  # pip install python-dotenv

# Necessary intents (permissions) for the bot to function
intents = discord.Intents.default()
intents.members = True  # permission to see server members
intents.message_content = True  # permission to read message content

# Set up the bot object and its descriptions
bot_status = "With Fate | Try !help "
bot_description = "This is the full help description"
bot = commands.Bot(command_prefix="!", description=bot_description, intents=intents, activity=discord.Game(name=bot_status))

# Load all cogs inside the cogs folder
async def load_cogs():
    print("\n------------------ Loading Cogs -----------------")
    text = input("please list all folders to load separated by commas (general folder is always loaded)\n")
    folder_names = text.split(',')
    print("loading folders: " + str(folder_names))
    for folder in os.listdir("cogs"):
        if str(folder) not in folder_names and str(folder) != "general":
            # since this is fast startup, we don't want to touch the general stuff except for faststartup.py
            print("skipping " + str(folder))
            continue
        print("parsing " + str(folder))
        for filename in os.listdir(os.path.join(f"cogs/{folder}")):
            if str(folder) == "general" and str(filename) != "faststartup.py":
                print("skipping file " + str(filename) + " because it's in general folder and not faststartup.py")
                continue
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
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
