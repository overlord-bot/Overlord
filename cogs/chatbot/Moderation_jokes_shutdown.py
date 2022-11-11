# Basic Chat Response
import random 
#from discord.ext import tasks
from discord.ext import commands
import discord
import json
import os

from bot import Bot


class TimChat(commands.Cog, name="TimChat"):
    """Basic Chatbot Functions"""

    def __init__(self, bot):
        self.bot = bot
        #self.taskLoop.start()
        self.index = 0

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='Friends')
        await member.add_roles(role)
        channel = discord.utils.get(member.guild.channels, name="new-friends")
        channel_id = channel.id
        channels = self.bot.get_channel(channel_id)
        await channels.send("Don't use dirty, inappropriate, NSFW languages or content in this server!")
        await channels.send("Enter agree or disagree to determine which way you go.")

        

#   def cog_unload(self):
#         self.taskLoop.cancel()

#     @tasks.loop(seconds=5)
#     async def taskLoop(self, message, arg):
#             message.channel.send(arg)
#             #print(self.index)
#             #self.index += 1


    @commands.command()
    async def pun(self, message):
        JOKES = ("My friend drove his expensive car into a tree and found out how his Mercedes bends.", "Never trust an atom, they make up everything!", "Why did Adele cross the road? To say hello from the other side.",
         "I don't trust stairs because they're always up to something.", "My friend's bakery burned down last night. Now his business is toast.", " I wasn't originally going to get a brain transplant, but then I changed my mind.", 
         "There was a kidnapping at school yesterday. Don't worry, though - he woke up!", "What washes up on tiny beaches? Microwaves.", "Do you know how to make holy water? You boil the hell out of it.", 
         "What does my head and hell have in common? They both have demons in them", "The teacher asked, 'why are you in school on a saturday?' I told her my mum told me to go to hell.", "What do you call a monkey that loves Doritos? A chipmunk!")
        await message.channel.send(random.choice(JOKES))
        #self.taskLoop.start(self,message, arg)
        

    @commands.command()
    async def goodbye(self, message):
        FAREWELL = ("See ya, ", "Bye bye, ", "See you around, ", "Alright, ", "Good to see you ", "Anytime ", "See you next time ")
        await message.channel.send(random.choice(FAREWELL) + message.author.name + ", have a great day!")
        await self.bot.close()
    
    @commands.command()
    async def test(self, message):
        dic = {"bj":30,"xh":23}
        json_f = json.dumps(dic)
        dir = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dir}/join_user.json", "w") as outwrite:
            outwrite.write(json_f)
        await message.channel.send("done")

async def setup(bot):
    await bot.add_cog(TimChat(bot))
