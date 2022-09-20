# Basic Chat Response

from discord.ext import commands
import webbrowser

class BasicChat(commands.Cog, name="Basic Chat"):
    """Basic Chatbot Functions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        elif message.content.startswith("hi"):
            await message.channel.send("hello")  # reacts with message in the location it was sent from
        elif message.content == "msg":
            await message.author.send('👋')  # sends a direct message to the user
        elif message.content == "react":
            await message.add_reaction("👍")  # adds an emoji reaction to a message, press windows key + '.' to bring up emoji list
            await message.add_reaction("❤")
            await message.add_reaction("🆗")
        elif message.content.lower().startswith("goodbye"):
            await message.channel.send("GoodBye")
            await self.bot.close()
        # not needed due to asyncio, left commented out in code in case needed later
        # await self.bot.process_commands(message)  # https://discordpy.readthedocs.io/en/stable/faq.html#why-does-on-message-make-my-commands-stop-working
        #additional features below
        elif "apex" in message.content.lower():
            await message.channel.send("Who's ready to fly on a zipline? I AM!")
            
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

async def setup(bot):
    await bot.add_cog(BasicChat(bot))
    await bot.add_cog(ExtraFunc(bot))
