# Clone of the game wordle

from discord.ext import commands

class WordGame(commands.Cog, name="Word Game"):
    """Plays the word game that is similar to Wordle"""

    def __init__(self, bot):
        self.bot = bot
        self.word = "Jeans"

    @commands.command()
    async def getword(self, ctx):
        """Returns the test word. FOR DEBUG ONLY!"""
        await ctx.send("Jeans")

async def setup(bot):
    await bot.add_cog(WordGame(bot))