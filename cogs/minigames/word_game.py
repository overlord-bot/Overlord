# Clone of the game wordle

from discord.ext import commands

class WordGame(commands.Cog, name="Word Game"):
    """Plays the word game that is similar to Wordle"""

    def __init__(self, bot):
        self.bot = bot
        self.word = "Jeans"
        self.round = -1
        self.current_progress = []

    @commands.command()
    async def getword(self, ctx):
        """Returns the test word. FOR DEBUG ONLY!"""
        await ctx.send(self.word)

    ######################################################################
    #   !startGame
    ######################################################################

    @commands.command()
    async def start_game(self, ctx):
        """Starts the word game."""
        if (self.round >= 0):
            await ctx.send("Game already started!")
        else:
            self.round = 0
            # TODO: Add multiple words
            await ctx.send("Game Started!")

    ######################################################################
    #   !addWord
    ######################################################################

    

    ######################################################################
    #   !endGame
    ######################################################################

    @commands.command()
    async def end_game(self, ctx):
        """Ends the word game if not started"""
        if (self.round >= 0):
            self.round = -1
            self.current_progress = []
            await ctx.send("Game ended! The word was " + self.word)
        else:
            await ctx.send("The game hasn't started!")

    ######################################################################
    #   !checkStatus
    ######################################################################

async def setup(bot):
    await bot.add_cog(WordGame(bot))