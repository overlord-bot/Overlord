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
        # 0 represents place without a move, 1 represents move from player 1, 2 for player 2
        self.board = [[0]*9 for i in range(9)]

    """
    Blank state is presented by brown square
    User 1 is represented by white circle
    User 2 is represented by black circle
    """
    async def printBoardState(self, context):
        # build the string to send it all in one message
        output_string = ""
        for i in range(9):
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
            output_string += "\n"
        await context.send(output_string)

    @commands.command()
    async def go(self, context):
        if len(context.message.content.split()) != 2:
            await context.send("invalid command")
            return

        self.player1 = context.message.author.id
        self.player2 = context.message.content.split()[1][2:-1:]
        print(self.player1)
        print(self.player2)
        await self.printBoardState(context)
        await context.send("go command working!")

async def setup(bot):
    await bot.add_cog(GoMinigame(bot))