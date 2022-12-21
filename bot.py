# bot.py

import asyncio
import os
import sys

import discord  # pip install -U discord.py
from discord.ext import commands
from dotenv import load_dotenv  # pip install python-dotenv


class Bot(commands.Bot):
    def __init__(self) -> None:
        # If TESTING_SERVER_ID is an environment variable, this will set the app commands
        #   to only sync on the server id stored in that env var (see cogs/general/startup.py).
        #   Otherwise, app commands will sync globally (and take up to an hour to sync).
        load_dotenv()

        testing_server_id = os.getenv("TESTING_SERVER_ID")
        self.testing_server = discord.Object(testing_server_id) if testing_server_id else None

        # Necessary intents (permissions) for the bot to function
        intents = discord.Intents.default()
        intents.members = True  # permission to see server members
        intents.message_content = True  # permission to read message content

        # Set up the bot object and its descriptions
        bot_status = "With Fate | Try !help"
        bot_description = "Project Overlord"
        super().__init__(command_prefix="!", description=bot_description, intents=intents,
                         activity=discord.Game(name=bot_status))

    async def setup_hook(self) -> None:
        await load_cogs(self)


# loads all subdirectories of folder, and loads all .py files that are inside a specified folder to load
async def load_folder(bot, folder, folder_names, flag_loadall):
    if folder.split('/')[-1] in folder_names or flag_loadall:
        print("loading folder: " + folder.split('/')[-1])

    # traversing all files within directory
    for file in os.listdir(os.path.join(f"{folder}")):
        # load all subdirectories
        if os.path.isdir(f"{str(folder)}/{file}") and not file.startswith("_") and not file.startswith("."):
            if folder.split('/')[-1] in folder_names:
                await load_folder(bot, folder + "/" + file, folder_names, True)
            await load_folder(bot, folder + "/" + file, folder_names, flag_loadall)
            continue

        # if the content of this folder should be loaded:
        elif folder.split('/')[-1] in folder_names or flag_loadall:
            if file.endswith(".py"):
                try:
                    await bot.load_extension(f"{folder.replace('/', '.')}.{file[:-3]}")
                    print(f"Success Loading: {folder}/{file}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed Loading: {folder}/{file} | Error: {exception}")


# Load all cogs inside the cogs folder
async def load_cogs(bot):
    print("\n------------------ Loading Cogs -----------------")
    arguments = sys.argv
    flag_loadall = False

    # adds folders specified to load from command line arguments into [folder_names]
    folder_names = []

    if "-all" in arguments or "-load" not in arguments:
        print(f"{'-all flag found,' if '-all' in arguments else 'no args specified,'} loading all modules \\(^.^)/")
        flag_loadall = True

    else:
        for i in range(0, len(arguments) - 1):
            if arguments[i] == "-load":
                folder_names = arguments[i + 1].split(",")
                folder_names = [name.strip() for name in folder_names]
                print("loading folders specified from command line input: " + str(folder_names))

    folder_names.append("general") # always load the general folder

    print("loading folders: " + str(folder_names))
    await load_folder(bot, os.path.join("cogs"), folder_names, flag_loadall)


def main():
    bot = Bot()
    load_dotenv()
    asyncio.run(bot.run(os.getenv("DISCORD_TOKEN")))  # fetches token from env file stored locally and starts bot


if __name__ == "__main__":
    main()