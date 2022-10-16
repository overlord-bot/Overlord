import discord
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
        self.curr_player_sign = "x"

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

    # get a list of indices of free cells
    def get_free_cells(self):
        free_cells = []

        # flat index
        i = 0

        for row in self.board:
            for cell in row:
                if cell is None:
                    free_cells.append(i)

                i += 1

        return free_cells

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

    # places an X/O at the specified location for the current player
    def make_move(self, flat_index):
        # reject move if specified cell is filled
        if flat_index not in self.get_free_cells():
            return

        # transform flat index into row-column pair
        row_index = flat_index // 3
        col_index = flat_index % 3

        # place current player's sign
        self.board[row_index][col_index] = self.curr_player_sign

        # switch current player
        if self.curr_player_sign == "x":
            self.curr_player_sign = "o"
        else:
            self.curr_player_sign = "x"

class TicTacToe(commands.Cog, name="Tic-tac-toe"):
    """A game of tic-tac-toe"""

    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @commands.command()
    async def tttnew(self, context, opponent: discord.User):
        """
        Start a new game by pinging someone, with yourself as X and your
        opponent as O.
        """

        # check against the user starting a game with themself
        if context.author == opponent:
            await context.reply("You can't play a game against yourself!")
            return

        # make sure the opponent is not a bot
        if opponent.bot:
            await context.reply("You can't play with bots!")
            return

        key = tuple(sorted([context.author.id, opponent.id]))

        # check that there is no active game between the two
        if key in self.active_games:
            await context.reply("You already have a game with them!")
            return

        self.active_games[key] = TicTacToeState(context.author, opponent)

    @commands.command()
    async def tttstop(self, context, opponent: discord.User):
        """
        Ends your game with the specified opponent if such a game is in
        progress.
        """

        key = tuple(sorted([context.author.id, opponent.id]))

        if key in self.active_games:
            del self.active_games[key]
            await context.reply(f"Ended game with <@!{opponent.id}>")
        else:
            await context.reply("You don't have a game with them!")

async def setup(bot):
    await bot.add_cog(TicTacToe(bot))
