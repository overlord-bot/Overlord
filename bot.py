# bot.py

import asyncio
import os
import sys
import discord  # pip install -U discord.py
from discord.ext import commands
from dotenv import load_dotenv  # pip install python-dotenv


class Bot(commands.Bot):
    def __init__(self) -> None:
        self.testing_server = None
        load_dotenv()
        # self.testing_server = discord.Object(os.getenv("TESTING_SERVER_ID"))

        # Necessary intents (permissions) for the bot to function
        intents = discord.Intents.default()
        intents.members = True  # permission to see server members
        intents.message_content = True  # permission to read message content

        # Set up the bot object and its descriptions
        bot_status = "With Fate | Try !help "
        bot_description = "This is the full help description"
        super().__init__(command_prefix="!", description=bot_description, intents=intents,
                         activity=discord.Game(name=bot_status))

    async def setup_hook(self) -> None:
        await load_cogs(self)


# MAIN STARTUP FUNCTION FOR A REGULAR STARTUP, treat this as you would treat main()
def main_standard():
    bot = Bot()
    load_dotenv()
    asyncio.run(bot.run(os.getenv("DISCORD_TOKEN")))  # fetches token from env file stored locally and starts bot


# Load all cogs inside the cogs folder
async def load_cogs(bot):
    print("\n------------------ Loading Cogs -----------------")
    arguments = sys.argv  # checking command line arguments
    print("your command line arguments:" + str(arguments))

    loadall = False
    flag_noargs = True
    for i in range(0, len(arguments)):
        if arguments[i] == "-all":
            flag_noargs = False
            print("found -all in command line input, loading all modules")
            loadall = True
            folder_names = ["all"]
            break
        if arguments[i] == "-load" and len(arguments) > i + 1:
            flag_noargs = False
            folder_names = arguments[i + 1].split(",")
            print("loading folders specified from command line input: " + str(folder_names))

    if flag_noargs:  # if no arguments provided, load everything
        print("no arguments received, loading all modules \\(^.^)/")
        folder_names = ["all"]

    if len(folder_names) > 0 and folder_names[0] == "all":  # detects if load all is selected
        print("loadall activated")
        loadall = True

    # loadall = False #hard disables loadall

    print("loading folders: " + str(folder_names))
    for folder in os.listdir("cogs"):
        if str(folder) not in folder_names and str(folder) != "general" and not loadall:  # general folder always loads
            print("skipping " + str(folder))
            continue
        print("parsing " + str(folder))
        for filename in os.listdir(os.path.join(f"cogs/{folder}")):
            if "-fast" in arguments and str(
                    folder) == "general" and filename != "startup.py":  # fast mode skips all but startup.py in general folder
                print(f"skipping file {filename}")
                continue
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{folder}.{filename[:-3]}")
                    print(f"Success Loading: cogs.{folder}.{filename}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed Loading: cogs.{folder}.{filename} | Error: {exception}")

'''
# IGNORE IF YOU'RE NOT USING COMMANDLESS FAST LOAD

def main_fast():
    # Necessary intents (permissions) for the bot to function
    intents = discord.Intents.default()
    intents.members = True  # permission to see server members
    intents.message_content = True  # permission to read message content

    # Set up the bot object and its descriptions
    bot_status = "alone"
    bot_description = "fastbot version"
    bot = commands.Bot(command_prefix="!", description=bot_description, intents=intents,
                       activity=discord.Game(name=bot_status))
    asyncio.run(fast_initialize(bot))


# IGNORE IF YOU'RE NOT USING COMMANDLESS FAST LOAD
async def fast_initialize(bot):
    await load_cogs(bot)
    load_dotenv()
    await bot.start(os.getenv("DISCORD_TOKEN"))

'''


def main():
    arguments = sys.argv
    if "-fast" in arguments:
        print("loading fastbot!")
        # main_fast()
    else:
        print("loading standard bot!")
        main_standard()


# only runs if this class is the startup file
if __name__ == "__main__":
    main()
