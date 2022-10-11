# Go minigame

"""
Outline for the game:

User 1 should be able to challenge another person, User 2, to a game of go via the follow command:
!go @User2

The bot will then send a 9x9 board of brown square emojis.

User 1 can then type in the command '!go (1,1)' to fill in the square at (1,1).
The bot will then print an updated board will (1,1) coordinate as a white circle emoji

User 2 can then input his move with a similar command
the bot will once again output the updated board

The bot will check and prevent invalid moves and ignore anyone outside of User 1 and User 2 trying to play

Play until game ends and the bot will count up the pieces to declare the winner.
"""

from discord.ext import commands

class GoMinigame(commands.Cog, name = "Go"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.player1 = None
        self.player2 = None
        self.turn = 1
        self.unplayedTiles = 81
        self.gameStarted = False
        # 0 represents place without a move, 1 represents move from player 1, 2 for player 2
        self.board = [[0]*9 for i in range(9)]

    """
    Blank state is presented by brown square
    User 1 is represented by white circle
    User 2 is represented by black circle
    """
    async def printBoardState(self, context):
        number = [
            ":stop_button:",
            ":one:",
            ":two:",
            ":three:",
            ":four:",
            ":five:",
            ":six:",
            ":seven:",
            ":eight:",
            ":nine:",
            ":stop_button:"
        ]

        # build the string to send it all in one message
        output_string = ":fast_forward:" * 4 + ":regional_indicator_g::regional_indicator_o::arrows_counterclockwise:" + ":rewind:" * 4 + "\n"

        for i in range(11):
            output_string += number[i]

        output_string += "\n"
        for i in range(9):
            output_string += number[9-i]
            for j in range(9):
                match self.board[i][j]:
                    case 0:
                        output_string += ":brown_square:"
                    case 1:
                        output_string += ":white_circle:"
                    case 2:
                        output_string += ':black_circle:'
                    case _:
                        output_string += 'There is a major problem!!'
            output_string += number[9-i] + "\n"

        for i in range(11):
            output_string += number[i]

        await context.send(output_string)

    @commands.command()
    async def go(self, context):
        #error checking for invalid commands
        if len(context.message.content.split()) != 2:
            await context.send("invalid command, must only have 2 commands")
            return
        if context.message.mentions == [] and self.gameStarted == False:
            await context.send("please tag another user")
            return

        #making a move
        if context.message.mentions == []:
            print("EPIC")
            await self.makeMove(context, context.message.content.split()[1])
            return

        #starting the game, resetting the board
        self.player1 = context.message.author
        self.player2 = context.message.mentions[0]
        self.board = [[0]*9 for i in range(9)]
        self.gameStarted = True
        self.turn = 1
        self.unplayedTiles = 81

        print(self.player1)
        print(self.player2)
        await self.printBoardState(context)
        await context.send("go command working!")

    async def makeMove(self, context, move):
        user = context.message.author
        if (self.turn == 1 and user != self.player1) or (self.turn == 2 and user != self.player2):
            print("Not the right player!")
            return
        if len(move) != 5:
            await context.send("Please write your move command like '(x,y)'")
            return

        x = int(move[1])
        y = int(move[3])

        if self.turn == 1:
            self.board[x][y] = 1
            self.turn = 2
        else:
            self.board[x][y] = 2
            self.turn = 1
        await self.printBoardState(context)

async def setup(bot):
    await bot.add_cog(GoMinigame(bot))