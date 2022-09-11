# Basic Chat Response

from discord.ext import commands


class BasicChat(commands.Cog, name="BasicChat"):
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

        # not needed due to asyncio, left commented out in code in case needed later
        # await self.bot.process_commands(message)  # https://discordpy.readthedocs.io/en/stable/faq.html#why-does-on-message-make-my-commands-stop-working


async def setup(bot):
    await bot.add_cog(BasicChat(bot))
