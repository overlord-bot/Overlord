# bot.py

import asyncio
import os
import platform

import discord
from discord.ext import commands

from dotenv import load_dotenv  # pip install python-dotenv


bot_status = "With Fate | Try !help "
bot_description = "This is the full help description"

intents = discord.Intents.default()
intents.members = True  # permission to see server members
intents.message_content = True  # permission to read message content

bot = commands.Bot(command_prefix="!", description=bot_description, intents=intents, activity=discord.Game(name=bot_status))


@bot.event
async def on_ready():
    print("------------------------------------------------------------------")
    print(f"{bot.user} (ID: {bot.user.id}) has connected to Discord!")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("------------------------------------------------------------------")


@bot.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f"Welcome {member.mention} to {guild.name}!"
        await guild.system_channel.send(to_send)


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    elif message.content.startswith("hi"):
        await message.channel.send("hello")  # reacts with message in the location it was sent from
    elif message.content == "msg":
        await message.author.send('👋')  # sends a direct message to the user
    elif message.content == "react":
        await message.add_reaction("👍")  # adds an emoji reaction to a message, press windows key + '.' to bring up emoji list
        await message.add_reaction("❤")
        await message.add_reaction("🆗")

    await bot.process_commands(message)  # https://discordpy.readthedocs.io/en/stable/faq.html#why-does-on-message-make-my-commands-stop-working


async def load():
    for folder in os.listdir("cogs"):
        print(folder)
        for filename in os.listdir(os.path.join(f"cogs/{folder}")):
            print(filename)
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{folder}.{filename[:-3]}")
                print(f"cogs.{folder}.{filename[:-3]}")


async def main():
    await load()

    load_dotenv()
    await bot.start(os.getenv("DISCORD_TOKEN"))  # fetches token from env file stored locally and starts bot

asyncio.run(main())


