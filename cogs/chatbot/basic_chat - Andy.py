# Chat Functions made by Andy

from discord.ext import commands

name_to_url = {"!youtube": "https://www.youtube.com/", '!yt': "https://www.youtube.com/",
               "!facebook": "https://www.facebook.com/", "!fb": "https://www.facebook.com/",
               "!reddit": "https://www.reddit.com/", "!lms": "https://lms.rpi.edu/",
               "!quacs": "https://quacs.org/", "!sis": "https://sis.rpi.edu/",
               "!gmail": "https://mail.google.com/mail/", "!pollbuddy": "https://pollbuddy.app/",
               "!webmail": "https://webmail.rpi.edu/", "!submitty": "https://submitty.cs.rpi.edu/home",
               "!sheets": "https://docs.google.com/spreadsheets/", "!docs": "https://docs.google.com/document/",
               "!google": "https://www.google.com/", "!twitter": "https://twitter.com/",
               "!instagram": "https://www.instagram.com/", "!ig": "https://www.instagram.com/",
               "!amazon": "https://www.amazon.com/"}

gifs_react = {"johncena": "https://media.giphy.com/media/zgJj5O3peaTrg95T46/giphy.gif",
              "marty": "https://media.giphy.com/media/yGoHdRNjnV7ze7LQfN/giphy.gif",
              "trump": "https://media.giphy.com/media/xTiTnHXbRoaZ1B1Mo8/giphy.gif",
              "biden": "https://media.giphy.com/media/QWw4hc5gTnJhY0BUI3/giphy.gif",
              "obama": "https://media.giphy.com/media/cEYFeDKVPTmRgIG9fmo/giphy.gif",
              "lebron": "https://media.giphy.com/media/GS2HlaP8SzW0g/giphy.gif",
              "turner": "https://media.giphy.com/media/tzV14WYQwgDQ61GCvt/giphy.gif",
              "kuzman": "https://media.giphy.com/media/7PbdlEW2fyXDubicsU/giphy.gif",
              "therock": "https://media.giphy.com/media/26ghbWoXv3G6ypo8o/giphy.gif",
              "hillaryclinton": "https://media.giphy.com/media/l0HlE56oAxpngfnWM/giphy.gif"}


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
        for key_ in gifs_react:
            if key_ in msg.replace(' ', ''):
                await message.reply(gifs_react[key_])



async def setup(bot):
    await bot.add_cog(AndyChat(bot))
