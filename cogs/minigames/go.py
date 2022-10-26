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

# string of either black or white pieces
class String:
    def __init__(self, player) -> None:
        self.points = []
        self.player = player

    def addPoint(self, x, y) -> None:
        self.points.append([x,y])

    def libertyCheck(self, board) -> bool:
        dir = [0,1,0,-1,0]
        for point in self.points:
            for i in range(4):
                x = point[0] + dir[i]
                y = point[1] = dir[i+1]
                if x < 0 or x > 8:
                    continue
                elif y < 0 or y > 8:
                    continue
                elif board[x][y] != 0 and self.player != board[x][y]:
                    return False
        return True
    
    def combineStrings(self, string):
        self.points = self.points + string.points


class GoMinigame(commands.Cog, name = "Go"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.player1 = None
        self.player2 = None
        self.turn = 1
        self.unplayedTiles = 81
        self.gameStarted = False
        self.passMove = 0

        # this keeps track of all strings of pieces present on the board
        self.stringMatch = {}
        self.stringBoard = [[-1]*9 for i in range(9)]
        self.stringCounter = 0

        # 0 represents place without a move, 1 represents move from player 1, 2 for player 2
        self.board = [[0]*9 for i in range(9)]
        # TESTING BOARD
        # self.board = [[2,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

    """
    Blank state is presented by brown square
    User 1 is represented by black circle
    User 2 is represented by white circle
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
                        output_string += ":black_circle:"
                    case 2:
                        output_string += ":white_circle:"
                    case _:
                        output_string += "There is a major problem!!"
            output_string += number[9-i] + "\n"

        for i in range(11):
            output_string += number[i]

        await context.send(output_string)

    # resets the state of the board
    def reset(self):
        print("game ended!")
        self.player1 = None
        self.player2 = None
        self.turn = 1
        self.unplayedTiles = 81
        self.gameStarted = False
        self.board = [[0]*9 for i in range(9)]

    # ends the game by checking the score of both players and returns tuple of (1st player score, 2nd player score)
    def endGame(self):
        return (0,0)

    # primary go command, used for: starting game, making move, and ending game
    @commands.command()
    async def go(self, context):
        #error checking for invalid commands
        if len(context.message.content.split()) != 2:
            await context.send("invalid command, must only have 2 commands")
            return

        if self.gameStarted == True and context.message.content.split()[1] == "pass" and (context.message.author == self.player1 or context.message.author == self.player2):
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
            self.passMove += 1

            if self.passMove == 2:
                result = self.endGame()
                self.reset()
                await context.send("Game ended! GG!")
                return

        #making a move
        if context.message.mentions == []:
            await self.makeMove(context, context.message.content.split()[1])
            return

        if context.message.mentions == [] and self.gameStarted == False:
            await context.send("please tag another user")
            return

        # starting the game, resetting the board
        # comment out if testing with board states
        self.reset()
        self.player1 = context.message.author
        self.player2 = context.message.mentions[0]
        self.gameStarted = True

        print(self.player1)
        print(self.player2)
        await self.printBoardState(context)
        await context.send("Game Started:")

    async def makeMove(self, context, move):
        user = context.message.author
        if (self.turn == 1 and user != self.player1) or (self.turn == 2 and user != self.player2):
            print("Not the right player!")
            return
        if len(move) != 5:
            await context.send("Please write your move command like '(x,y)'")
            return

        self.passMove = 0
        x = 9-int(move[3])
        y = int(move[1])-1
        
        if x < 0 or x > 8 or y < 0 or y > 8 or self.board[x][y] != 0:
            await context.send("Invalid move, please pick a valid tile")
            return

        self.board[x][y] = self.turn

        # the following checks for surrounding strings and updates them
        dir = [0,1,0,-1,0]
        neighboringStrings = []
        for i in range(4):
            j = x + dir[i]
            k = y + dir[i+1]
            if j < 0 or j > 8:
                continue
            elif k < 0 or k > 9:
                continue
            elif self.board[j][k] == 0:
                continue
            # checks if any of the strings around have no liberties and if so, those pieces are eliminated
            elif self.board[j][k] != self.turn:
                string = self.stringMatch[self.stringBoard[j][k]]
                # eliminates string and resets it in our internal representation
                if string.libertyCheck(self.board) == True:
                    del self.stringMatch[self.stringBoard[j][k]]
                    for point in string.points:
                        self.stringBoard[point[0]][point[1]] = -1
                        self.board[point[0]][point[1]] = 0
            # this means that 
            else:
                neighboringStrings.append(self.stringBoard[j][k])

        # remove duplicates
        setNeighbors = list(set(neighboringStrings))
        if len(setNeighbors) == 0:
            self.stringMatch[self.stringCounter] = String(self.turn)
            self.stringMatch[self.stringCounter].addPoint(x,y)
            self.stringBoard[x][y] = self.stringCounter
            self.stringCounter += 1
        else:
            self.stringMatch[setNeighbors[0]].addPoint(x,y)
            for i in range(1,len(setNeighbors)):
                self.stringMatch[setNeighbors[0]].combineStrings(self.stringMatch[setNeighbors[i]])

        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

        await self.printBoardState(context)

        self.unplayedTiles -= 1
        if self.unplayedTiles == 0:
            result = self.endGame()
            self.reset()
            await context.send("Game ended! GG!")

async def setup(bot):
    await bot.add_cog(GoMinigame(bot))