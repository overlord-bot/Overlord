# Chat Functions made by Andy

from discord.ext import commands

name_to_url = {"!youtube": "https://www.youtube.com/", '!yt': "https://www.youtube.com/",
               "!facebook": "https://www.facebook.com/", "!fb": "https://www.facebook.com/",
               "!reddit": "https://www.reddit.com/", "!lms": "https://lms.rpi.edu/",
               "!quacs": "https://quacs.org/", "!sis": "https://sis.rpi.edu/"}


class AndyChat(commands.Cog, name="Andy Chat"):
    """Andy Chatbot Functions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        msg = message.content.lower()

        # reacts with a specified emoji
        if msg.startswith("!react"):
            await message.add_reaction(message.content[-1])

        # finds website name in dictionary and sends a link
        if msg in name_to_url.keys():
            await message.reply(name_to_url[msg])

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
