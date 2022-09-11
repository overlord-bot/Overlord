# bot.py

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # fetches token from env file stored locally

bot_status = "With Fate | Try !help "
bot_description = "This is the full help description"

intents = discord.Intents.default()
intents.members = True  # permission to see server members
intents.message_content = True  # permission to read message content

bot = commands.Bot(command_prefix='!', description=bot_description, intents=intents, activity=discord.Game(name=bot_status))


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.startswith("hi"):
        await message.channel.send('hello')  # reacts with message in the location it was sent from
    elif message.content == 'msg':
        await message.author.send('👋')  # sends a direct message to the user
    elif message.content == 'react':
        await message.add_reaction('👍')  # adds a emoji reaction to a message, press windows key + '.' to bring up emoji list
        await message.add_reaction('❤')
        await message.add_reaction('🆗')

    await bot.process_commands(message)  # https://discordpy.readthedocs.io/en/stable/faq.html#why-does-on-message-make-my-commands-stop-working

bot.run(TOKEN)
