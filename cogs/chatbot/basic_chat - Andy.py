# Basic Chat Response
import random 
import random 
import io
import aiohttp
import discord

from discord.ext import commands


class AndyChat(commands.Cog, name="Andy Chat"):
    """Andy Chatbot Functions"""

    def __init__(self, bot):
        self.bot = bot

        
    @commands.Cog.listener()

    async def on_message(self, message):

        ID = message.author.id

        # gifs
        if message.content.lower().startswith("what") and len(message.content) < 10:
            await message.reply("https://media.giphy.com/media/zgJj5O3peaTrg95T46/giphy.gif")

        elif "johncena" in message.content.lower().replace(" ", ""):
            await message.reply("https://media.giphy.com/media/xTiTnoHt2NwerFMsCI/giphy.gif")

        elif "shirley" in message.content.lower():
            await message.reply("https://media.giphy.com/media/dHvG5FzLhmwJS3CUZj/giphy.gif")
        
        elif "marty" in message.content.lower():
            await message.reply("https://media.giphy.com/media/yGoHdRNjnV7ze7LQfN/giphy.gif")

        elif "trump" in message.content.lower():
            await message.reply("https://media.giphy.com/media/xTiTnHXbRoaZ1B1Mo8/giphy.gif")

        elif "biden" in message.content.lower():
            await message.reply("https://media.giphy.com/media/QWw4hc5gTnJhY0BUI3/giphy.gif")

        elif "obama" in message.content.lower():
            await message.reply("https://media.giphy.com/media/cEYFeDKVPTmRgIG9fmo/giphy.gif")

        elif "lebron" in message.content.lower():
            await message.reply("https://media.giphy.com/media/GS2HlaP8SzW0g/giphy.gif")

        elif "turner" in message.content.lower():
            await message.reply("https://media.giphy.com/media/tzV14WYQwgDQ61GCvt/giphy.gif")

        elif "kuzman" in message.content.lower():
            await message.reply("https://media.giphy.com/media/7PbdlEW2fyXDubicsU/giphy.gif")

            



async def setup(bot):
    await bot.add_cog(AndyChat(bot))
