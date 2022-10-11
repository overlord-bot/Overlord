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

       
        # reacts with the a specified emoji
        if message.content.lower().startswith("!react"):
                await message.add_reaction(message.content[-1])

        # replys with a link to website

        if message.content.lower().startswith("!reddit"):
            await message.reply("https://www.reddit.com/")

        elif message.content.lower().startswith("!youtube"):
            await message.reply("https://www.youtube.com/")
        
        elif message.content.lower().startswith("!yt"):
            await message.reply("https://www.youtube.com/")

        elif message.content.lower().startswith("!facebook"):
            await message.reply("https://www.facebook.com/")

        elif message.content.lower().startswith("!fb"):
            await message.reply("https://www.facebook.com/")

        elif message.content.lower().startswith("!lms"):
            await message.reply("https://lms.rpi.edu/")

        elif message.content.lower().startswith("!quacs"):
            await message.reply("https://quacs.org/")

        elif message.content.lower().startswith("!sis"):
            await message.reply("https://sis.rpi.edu/")


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

        elif "therock" in message.content.lower().replace(' ', ''):
            await message.reply("https://media.giphy.com/media/26ghbWoXv3G6ypo8o/giphy.gif")

            



async def setup(bot):
    await bot.add_cog(AndyChat(bot))
