from discord.ext import commands

class TicTacToeState:
    def __init__(self):
        pass

class TicTacToe(commands.Cog, name="Tic-tac-toe"):
    """A game of tic-tac-toe"""

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(TicTacToe(bot))
