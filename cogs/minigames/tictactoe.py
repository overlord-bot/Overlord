from discord.ext import commands

class TicTacToeState:
    def __init__(self, player_x, player_o):
        # initialise the board to be empty
        self.board = [[None] * 3 for i in range(3)]

        # record who is playing
        self.players = {
            "x": player_x,
            "o": player_o
        }

        # X always has the first turn
        self.curr_player = player_x

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

    # checks if all spaces have been filled
    def is_filled(self):
        for row in self.board:
            if None in row:
                return False

        return True

    # gets the player by their associated letter, if possible
    def get_player(self, letter):
        if (letter == "x") or (letter == "o"):
            return self.players[letter]
        else:
            return None

    # determines who has won, if at all
    def get_winner(self):
        # check each row
        for row in self.board:
            # all the same value?
            if len(set(row)) == 1:
                return self.get_player(row[0])

        # check each column
        for i in range(3):
            # get unique values
            values = {self.board[0][i], self.board[1][i], self.board[2][i]}

            # all the same value?
            if len(values) == 1:
                return self.get_player(self.board[0][i])

        # check diagonal from top left to bottom right
        diagonal_values = {self.board[0][0], self.board[1][1], self.board[2][2]}

        if len(diagonal_values) == 1:
            return self.get_player(self.board[0][0])

        # check diagonal from top right to bottom left
        diagonal_values = {self.board[0][2], self.board[1][1], self.board[2][0]}

        if len(diagonal_values) == 1:
            return self.get_player(self.board[0][2])

        # no winner yet
        return None

class TicTacToe(commands.Cog, name="Tic-tac-toe"):
    """A game of tic-tac-toe"""

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(TicTacToe(bot))
