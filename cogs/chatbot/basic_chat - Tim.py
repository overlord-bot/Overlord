# Basic Chat Response
import random 
from discord.ext import commands
import datetime
from datetime import date


class TimChat(commands.Cog, name="TimChat"):
    """Basic Chatbot Functions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        BAD_WORDS = ("fuck", "motherfucker", "shit")

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
        
        elif (message.content.lower() == "what day is today?") or (message.content.lower() == "what day is today") or (message.content.lower() == "what is today?") or (message.content.lower() == "date") or (message.content.lower() == "what is the date"):
            today = date.today()
            d = today.strftime("%B %d, %Y")
            await message.channel.send("Today is " + d)

        elif (message.content.lower() == "who's the leader?") or (message.content.lower() == "leader of the program") or (message.content.lower() == "leader"):
            await message.channel.send("Master Jack & Master Alan")
            await message.channel.send("Any words that disrespect this channel will be deleted and warning message will be send!")
            
        for word in message.content.lower().split():
            if word.lower() in BAD_WORDS:
                await message.delete()
                await message.channel.send("https://c.tenor.com/fzrYWO2l7KkAAAAC/captain-america-language.gif")
                await message.channel.send("Watch your language!")
    
    @commands.command()
    async def pun(self, message):
        JOKES = ("My friend drove his expensive car into a tree and found out how his Mercedes bends.", "Never trust an atom, they make up everything!", "Why did Adele cross the road? To say hello from the other side.",
         "I don't trust stairs because they're always up to something.", "My friend's bakery burned down last night. Now his business is toast.", " I wasn't originally going to get a brain transplant, but then I changed my mind.", 
         "There was a kidnapping at school yesterday. Don't worry, though - he woke up!", "What washes up on tiny beaches? Microwaves.", "Do you know how to make holy water? You boil the hell out of it.", 
         "What does my head and hell have in common? They both have demons in them", "The teacher asked, 'why are you in school on a saturday?' I told her my mum told me to go to hell.", "What do you call a monkey that loves Doritos? A chipmunk!")
        await message.channel.send(random.choice(JOKES))
    @commands.command()
    async def goodbye(self, message):
        FAREWELL = ("See ya, ", "Bye bye, ", "See you around, ", "Alright, ", "Good to see you ", "Anytime ", "See you next time ")
        await message.channel.send(random.choice(FAREWELL) + message.author.name + ", have a great day!")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(TimChat(bot))
