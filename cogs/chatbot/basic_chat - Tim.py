# Basic Chat Response
import random 
from discord.ext import commands
from datetime import datetime
from datetime import date


class TimChat(commands.Cog, name="Basic Chat"):
    """Basic Chatbot Functions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        elif message.content.lower().startswith("hi"):
            await message.channel.send("Great " + message.author.name + " !")  # reacts with message in the location it was sent from
        elif message.content == "msg":
            await message.author.send('👋')  # sends a direct message to the user
        elif message.content == "react":
            await message.add_reaction("👍")  # adds an emoji reaction to a message, press windows key + '.' to bring up emoji list
            await message.add_reaction("❤")
            await message.add_reaction("🆗")
        # not needed due to asyncio, left commented out in code in case needed later
        # await self.bot.process_commands(message)  # https://discordpy.readthedocs.io/en/stable/faq.html#why-does-on-message-make-my-commands-stop-working
        #additional features below
        elif (message.content == "what the time is it?") or (message.content == "what the time is it") or (message.content == "what time") or (message.content == "time"):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            await message.channel.send("It's " + current_time + " now!")
        
        elif (message.content.lower() == "what day is today?") or (message.content.lower() == "what day is today") or (message.content.lower() == "what is today?") or (message.content.lower() == "date"):
            today = date.today()
            d = today.strftime("%B %d, %Y")
            await message.channel.send("Today is " + d)

        elif "fuck" in message.content.lower():
            await message.delete()
            await message.channel.send("Watch your language!")

        elif (message.content.lower() == "goodbye") or (message.content.lower() == "good bye"):     #close the bot
            await message.channel.send("GoodBye, " + message.author.name + ", have a great day!")
            await self.bot.close()
<<<<<<< Updated upstream
            
            
class ExtraFunc(commands.Cog, name="Additional Function "):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()  
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        elif 'rick roll' in message.content.lower():
            await message.channel.send("Never Gonna Give You Up!")
            await message.channel.send("Never Gonna Let You Down!")
        GREETING_INPUTS = ("hello", "greetings", "sup", "what's up","hey","hi")
        for word in message.content.split():
            if word.lower() in GREETING_INPUTS:
                await message.channel.send(random.choice(GREETING_INPUTS))
=======

>>>>>>> Stashed changes
    
async def setup(bot):
    await bot.add_cog(TimChat(bot))
