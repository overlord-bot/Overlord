from discord.ext import commands

class TicTacToeState:
    def __init__(self):
        # initialise the board to be empty
        self.board = [[None] * 3 for i in range(3)]

    # get Discord-friendly string representation of the board
    def __str__(self):
        NUMBER_NAMES = ["one", "two", "three", "four", "five", "six", "seven",
            "eight", "nine"]

        stringified = ""

        # row-major counter for board's cells (0 to 9)
        counter = 0

        for row in self.board:
            for cell in row:
                stringified += f":{cell if cell else NUMBER_NAMES[counter]}:"
                counter += 1

            stringified += "\n"

        # strip excess whitespace
        return stringified.strip()

class TicTacToe(commands.Cog, name="Tic-tac-toe"):
    """A game of tic-tac-toe"""

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(TicTacToe(bot))
