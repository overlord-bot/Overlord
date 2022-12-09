# Chat Functions made by Andy

from re import A
from discord.ext import commands
from discord.ext import *
import giphy_client 
from giphy_client.rest import ApiException  

name_to_url = {"!s youtube": "https://www.youtube.com/", '!s yt': "https://www.youtube.com/",
               "!s facebook": "https://www.facebook.com/", "!s fb": "https://www.facebook.com/",
               "!s reddit": "https://www.reddit.com/", "!s lms": "https://lms.rpi.edu/",
               "!s quacs": "https://quacs.org/", "!s sis": "https://sis.rpi.edu/",
               "!s gmail": "https://mail.google.com/mail/", "!s pollbuddy": "https://pollbuddy.app/",
               "!s webmail": "https://webmail.rpi.edu/", "!s submitty": "https://submitty.cs.rpi.edu/home",
               "!s sheets": "https://docs.google.com/spreadsheets/", "!s docs": "https://docs.google.com/document/",
               "!s google": "https://www.google.com/", "!s twitter": "https://twitter.com/",
               "!s instagram": "https://www.instagram.com/", "!s ig": "https://www.instagram.com/",
               "!s amazon": "https://www.amazon.com/"}

gifs_react = {"johncena": "https://media.giphy.com/media/zgJj5O3peaTrg95T46/giphy.gif",
              "marty": "https://media.giphy.com/media/yGoHdRNjnV7ze7LQfN/giphy.gif",
              "trump": "https://media.giphy.com/media/xTiTnHXbRoaZ1B1Mo8/giphy.gif",
              "biden": "https://media.giphy.com/media/QWw4hc5gTnJhY0BUI3/giphy.gif",
              "obama": "https://media.giphy.com/media/cEYFeDKVPTmRgIG9fmo/giphy.gif",
              "lebron": "https://media.giphy.com/media/GS2HlaP8SzW0g/giphy.gif",
              "turner": "https://media.giphy.com/media/tzV14WYQwgDQ61GCvt/giphy.gif",
              "kuzman": "https://media.giphy.com/media/7PbdlEW2fyXDubicsU/giphy.gif",
              "therock": "https://media.giphy.com/media/26ghbWoXv3G6ypo8o/giphy.gif",
              "hillaryclinton": "https://media.giphy.com/media/l0HlE56oAxpngfnWM/giphy.gif",
              "ksi": "https://media.giphy.com/media/1MdRrNmfucoxnunjhN/giphy.gif",
              "spiderman": "https://giphy.com/clips/plusQA-test-partner-1iemyTrXywCBcE8WOi",
              "batman": "https://media.giphy.com/media/yuoeTyJ2qie2x3tvJL/giphy.gif",
              "superman": "https://media.giphy.com/media/R8MIGe47XWx68/giphy.gif"}

interactions = {"!slap @" : "https://media.giphy.com/media/uqSU9IEYEKAbS/giphy.gif",
                "!hug @" : "https://media.giphy.com/media/5OqXb948EBkyUcnwHt/giphy.gif",
                "!tackle @" : "https://media.giphy.com/media/l8ooOxhcItowwLPuZn/giphy.gif",
                "!high five @" : "https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif",
                "!fist bump @" : "https://media.giphy.com/media/hfYnqeqVeO4pO/giphy.gif",
                "!throw @" : "https://media.giphy.com/media/TFBisvdSNm3I8rwlqe/giphy.gif",
                "!wrestle @" : "https://media.giphy.com/media/1MjlDZmSsS8DVJj387/giphy.gif",
                "!eat @" : "https://media.giphy.com/media/l3UcD7vkCptuTGAX6/giphy.gif"}



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
        
        # interactions
        for key_ in interactions:
            if key_ in msg:
                msg_list = msg.split()
                await message.channel.send("{} {} {}".format(message.author.name, msg_list[0][1:] + 's', msg_list[1][1:]))
                await message.channel.send(interactions[key_])
        
        async def gif(ctx,*, q = "Smile"):
            api_key = 'gAjUHlVPfCnyPPRN7UHBCXzpSE3zaCJm'
            api_instance = giphy_client.DefaultApi()

            api_response = api_instance.gifs_search_get(api_key, q, limit = 5, rating = 'g')
            lst = list(api_response.data)
            giff = random.choice(lst)

            await ctx.channel.send(giff.embed_url)

        


async def setup(bot):
    await bot.add_cog(AndyChat(bot))
