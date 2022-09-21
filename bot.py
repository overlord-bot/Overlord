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

# Setup the bot object and its descriptions
bot_status = "With Fate | Try !help "
bot_description = "This is the full help description"
bot = commands.Bot(command_prefix="!", description=bot_description, intents=intents, activity=discord.Game(name=bot_status))

# If you are not planning on developing application or slash commands ignore this.
# FOR MAIN RELEASE CHANGE testing_server TO NONE OR FALSE
testing_server = discord.Object(id=333409598365106176)
#                                 ^^^^^^^^^^^^^^^^^^
#                               Insert your server id here
#                         (make sure discord dev mode is enabled)
# Click "Copy Id": https://i.gyazo.com/3499ab2ba0219b07e7e892355931c17a.png


# Load all cogs inside the cogs folder
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
