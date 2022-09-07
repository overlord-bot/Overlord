# bot.py

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # fetches token from env file stored locally

intents = discord.Intents.default()
intents.message_content = True  # permission to read message content

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    if message.content == 'hi':
        await message.channel.send('hello')


client.run(TOKEN)
