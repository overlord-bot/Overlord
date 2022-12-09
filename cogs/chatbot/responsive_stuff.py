# Basic Chat Response
import json
import random
from datetime import date, datetime

import discord
from discord.ext import commands


class BasicChat(commands.Cog, name="Basic Chat"):
    """Basic Chatbot Functions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        BAD_WORDS = ("fuck", "motherfucker", "shit", "fk", "mf", "fucking")

        if message.author == self.bot.user or message.author.bot:
            return
        elif message.content.lower() == "hi":
            await message.channel.send("Great " + message.author.name + " !")  # reacts with message in the location it was sent from
        elif message.content == "msg":
            await message.author.send('👋')  # sends a direct message to the user
        elif message.content == "react":
            await message.add_reaction("👍")  # adds an emoji reaction to a message, press windows key + '.' to bring up emoji list
            await message.add_reaction("❤")
            await message.add_reaction("🆗")
        elif 'rick roll' in message.content.lower():
            await message.channel.send("https://c.tenor.com/_4YgA77ExHEAAAAd/rick-roll.gif")
            await message.channel.send("Never Gonna Give You Up!")
            await message.channel.send("Never Gonna Let You Down!")
        elif (message.content == "what the time is it?") or (message.content == "what the time is it") or (message.content == "what time") or (message.content == "time"):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            await message.channel.send("It's " + current_time + " now!")
        
        elif (message.content.lower() == "what day is today?") or (message.content.lower() == "what day is today") or (message.content.lower() == "what is today?") or (message.content.lower() == "date") or (message.content.lower() == "what is the date"):
            today = date.today()
            d = today.strftime("%B %d, %Y")
            await message.channel.send("Today is " + d)

        elif (message.content.lower() == "who's the leader?") or (message.content.lower() == "leader of the program") or (message.content.lower() == "leader"):
            await message.channel.send("Master Jack & Master Alan")

        GREETING_INPUTS = ("hello", "greetings", "sup", "what's up","hey",)
        for word in message.content.split():
            if word.lower() in GREETING_INPUTS:
                await message.channel.send(random.choice(GREETING_INPUTS))
        # not needed due to asyncio, left commented out in code in case needed later
        # await self.bot.process_commands(message)  # https://discordpy.readthedocs.io/en/stable/faq.html#why-does-on-message-make-my-commands-stop-working
        #additional features below

        ctx = await self.bot.get_context(message)    
        for word in message.content.lower().split():
            if word.lower() in BAD_WORDS:
                await message.delete()
                muterole = discord.utils.get(ctx.guild.roles,name="Muted")
            
                if not muterole:
                    perms = discord.Permissions(speak = False, send_messages=False,read_messages=True)
                    muterole = await ctx.guild.create_role(name = "Muted",permissions=perms)
                    #for channel in ctx.guild.channels:
                        #await channel.set_permmissions(muterole, speak = False, send_message=False,read_messages=True)  
                group = {}
                with open("./cogs/chatbot/Roles.json","r") as f:
                    js=f.read()
                if len(js) == 0:
                    var = json.dumps(group)
                    f = open("./cogs/chatbot/Roles.json", "w")
                    f.write(var)
                    f.close()
                else:
                    group = json.loads(js) #Group dictionary
                data = {} #Detail data for each member
                
                
                Roles = []
                for role in message.author.roles:
                    if(role.name!="@everyone"):
                        Roles.append(role.id)
                
                data["was"] = Roles
                data["now"] = muterole.id
                data["Time"] = "Inappropriate Word(s)"
                group[str(message.author.id)] = data
                print(group)
                var = json.dumps(group)
                f = open("./cogs/chatbot/Roles.json", "w")
                f.write(var)
                f.close()
                'await Member.remove_roles(Member.roles) #Remove the role (object) from the user.  '
                await message.author.edit(roles=[muterole])
                'await Member.add_roles(muterole,reason=reasons)'
                await ctx.send(f"Muted {message.author.mention} for reason Inappropriate Word(s)") 
                await message.channel.send("https://c.tenor.com/fzrYWO2l7KkAAAAC/captain-america-language.gif")
                await message.channel.send("Watch your language!")
    
async def setup(bot):
    await bot.add_cog(BasicChat(bot))

