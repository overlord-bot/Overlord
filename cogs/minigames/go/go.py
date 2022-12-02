# Go minigame
from collections import deque 

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
                y = point[1] + dir[i+1]
                if x < 0 or x > 8:
                    pass
                elif y < 0 or y > 8:
                    pass
                elif board[x][y] == 0:
                    print(False)
                    return False
        print(True)
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

        self.player1LostStones = 0
        self.player2LostStones = 0

        # 0 represents place without a move, 1 represents move from player 1, 2 for player 2
        self.board = [[0]*9 for i in range(9)]

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
        self.stringMatch = {}
        self.stringBoard = [[-1]*9 for i in range(9)]
        self.stringCounter = 0
        self.player1LostStones = 0
        self.player2LostStones = 0
        self.passMove = 0

    # this helps with scoring at the end. we perform bfs at a point to see if it is surrounded by all one piece
    def BFS(self, starti, startj):
        dq = deque()
        visited = set()
        res = -1
        dir = [0,1,0,-1,0]

        dq.append((starti,startj))

        while dq:
            point = dq.popleft()
            visited.add(point)
            i = point[0]
            j = point[1]
            for a in range(4):
                x = i + dir[a]
                y = j + dir[a+1]
                if x > 8 or x < 0 or y > 8 or y < 0:
                    continue
                elif self.board[x][y] == 0:
                    if (x,y) not in visited:
                        dq.append((x,y))
                elif res == -1:
                    res = self.board[x][y]
                elif self.board[x][y] != res:
                    return -1

        return res

    # ends the game by checking the score of both players and returns tuple of (1st player score, 2nd player score)
    def endGame(self):
        p1 = 0
        p2 = 0
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    continue
                res = self.BFS(i,j)
                if res == 1:
                    p1 += 1
                elif res == 2:
                    p2 += 1
    
        # komi is given to player 2 since player 1 makes the first move and it prevents draws. Adjustable
        p2 += 7.5

        # we deduct the points for the pieces captured by the other player
        p1 -= self.player1LostStones
        p2 -= self.player2LostStones

        return (p1,p2)

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
                # A draw is not possible given komi
                if result[0] > result[1]:
                    await context.send("Player 1 won with " + str(result[0]) + " points compared to player 2's " + str(result[1]) + " points")
                else:
                    await context.send("Player 2 won with " + str(result[1]) + " points compared to player 1's " + str(result[0]) + " points")
                self.reset()
                await context.send("Game ended! GG!")
                return
            return

        #making a move
        if context.message.mentions == []:
            await self.makeMove(context, context.message.content.split()[1], False)
            return

        if context.message.mentions == [] and self.gameStarted == False:
            await context.send("please tag another user")
            return

        # starting the game, resetting the board
        self.reset()
        self.player1 = context.message.author
        self.player2 = context.message.mentions[0]
        self.gameStarted = True

        print(self.player1)
        print(self.player2)
        await self.printBoardState(context)
        await context.send("Game Started:")

        # FOR TESTING MOVES
        # await self.testMovesSuite(context)
        # await self.testSelfSurroundSuite(context)

    async def makeMove(self, context, move, test):
        if test == False:
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

        print("Move made: ("+ move[1] + "," + move[3] + ") by player " + str(self.turn))
        
        if x < 0 or x > 8 or y < 0 or y > 8 or self.board[x][y] != 0:
            await context.send("Invalid move, please pick a valid tile")
            return

        self.board[x][y] = self.turn

        # the following checks for surrounding strings and updates them
        dir = [0,1,0,-1,0]
        neighboringStrings = []
        totalLost = 0
        for i in range(4):
            j = x + dir[i]
            k = y + dir[i+1]
            if j < 0 or j > 8:
                continue
            elif k < 0 or k > 8:
                continue
            elif self.board[j][k] == 0:
                continue
            # checks if any of the strings around have no liberties and if so, those pieces are eliminated
            elif self.board[j][k] != self.turn:
                string = self.stringMatch[self.stringBoard[j][k]]
                lostPoints = len(string.points)
                # eliminates string and resets it in our internal representation
                if string.libertyCheck(self.board) == True:
                    totalLost += lostPoints
                    if self.turn == 1:
                        self.player2LostStones += lostPoints
                    else:
                        self.player1LostStones += lostPoints
                    del self.stringMatch[self.stringBoard[j][k]]
                    for point in string.points:
                        self.stringBoard[point[0]][point[1]] = -1
                        self.board[point[0]][point[1]] = 0
            # this means that there are still liberties available and we can append it
            else:
                neighboringStrings.append(self.stringBoard[j][k])

        # remove duplicates
        setNeighbors = list(set(neighboringStrings))
        stringNum = -1
        # the case where the new piece placed borders no new strings
        if len(setNeighbors) == 0:
            self.stringMatch[self.stringCounter] = String(self.turn)
            self.stringMatch[self.stringCounter].addPoint(x,y)
            self.stringBoard[x][y] = self.stringCounter
            stringNum = self.stringCounter
            self.stringCounter += 1
        else:
            # combining neighboring strings
            self.stringMatch[setNeighbors[0]].addPoint(x,y)
            self.stringBoard[x][y] = setNeighbors[0]
            stringNum = setNeighbors[0]
            for i in range(1,len(setNeighbors)):
                self.stringMatch[setNeighbors[0]].combineStrings(self.stringMatch[setNeighbors[i]])
                # update the board keeping track of the different strings
                for point in self.stringMatch[setNeighbors[0]].points:
                    self.stringBoard[point[0]][point[1]] = setNeighbors[0]
        
        # if the move did not eliminate any other pieces, we also have to check if the newly placed has liberties
        if totalLost == 0 and self.stringMatch[stringNum].libertyCheck(self.board) == True:
            numLost = len(self.stringMatch[stringNum].points)
            if self.turn == 1:
                self.player1LostStones += numLost
            else:
                self.player2LostStones += numLost
            await context.send(str(numLost) + " Pieces of Player " + str(self.turn) + " Were Captured!")
            for point in self.stringMatch[stringNum].points:
                self.stringBoard[point[0]][point[1]] = -1
                self.board[point[0]][point[1]] = 0
            del self.stringMatch[stringNum]
        elif totalLost > 0:
            await context.send(str(totalLost) + " Pieces of Player " + str(3-self.turn) + " Were Captured!")

        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

        # for debugging
        if test == True:
            for o in range(9):
                print(self.board[o])
            for o in range(9):
                print(self.stringBoard[o])
            print("STRINGS: ")
            for li in self.stringMatch.values():
                print(li.points)

        # disabled when debugging to make the code run faster
        if test == False:
            await self.printBoardState(context)

        self.unplayedTiles -= 1
        if self.unplayedTiles == 0:
            result = self.endGame()
            self.reset()
            await context.send("Game ended! GG!")

            if result[0] > result[1]:
                await context.send("Player 1 won with " + str(result[0]) + "points compared to player 2's " + str(result[1]) + "points")
            else:
                await context.send("Player 2 won with " + str(result[1]) + "points compared to player 1's " + str(result[0]) + "points")

    async def testMovesSuite(self, context):
        checkpoint1 = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [2,0,0,0,0,0,0,0,0],
            [0,2,0,0,0,0,0,0,0],
            [0,2,0,0,0,0,0,0,0]
        ]
        checkpoint2 = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0]
        ]
        checkpoint3 = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,2,0,0,0,0,0],
            [0,0,2,0,0,0,0,0,0],
            [0,0,1,2,0,0,0,0,0],
            [0,1,0,1,0,0,0,0,0],
            [1,0,1,1,0,0,0,0,0],
            [0,1,0,1,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0]
        ]
        checkpoint4 = [
            [0,0,0,1,0,0,0,2,0],
            [0,0,1,0,1,0,0,2,0],
            [0,1,0,0,0,1,2,0,0],
            [0,0,1,0,1,0,0,2,2],
            [0,1,0,1,0,0,0,0,0],
            [1,0,1,1,0,0,0,0,0],
            [0,1,0,1,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0]
        ]
        endstate = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ]
        # TEST CORNER SURROUND
        await self.makeMove(context, "(1,1)", True)
        await self.makeMove(context, "(1,3)", True)
        await self.makeMove(context, "(1,2)", True)
        await self.makeMove(context, "(2,2)", True)
        await self.makeMove(context, "(1,4)", True)
        await self.makeMove(context, "(2,1)", True)
        assert self.board == checkpoint1, "Checkpoint 1: Failed to cancel out corner pieces"
        # 2 corner pieces should be captured by player 2
        await self.makeMove(context, "(2,3)", True)
        await self.makeMove(context, "(1,2)", True)
        await self.makeMove(context, "(3,2)", True)
        await self.makeMove(context, "(1,1)", True)
        await self.makeMove(context, "(3,1)", True)
        assert self.board == checkpoint2, "Checkpoint 2: Failed to cancel out corner pieces"
        # 5 corner pieces should be captured by player 2

        # CENTER SURROUND
        await self.makeMove(context, "(2,4)", True)
        await self.makeMove(context, "(4,3)", True)
        await self.makeMove(context, "(3,3)", True)
        await self.makeMove(context, "(4,4)", True)
        await self.makeMove(context, "(3,5)", True)
        await self.makeMove(context, "(3,6)", True)
        await self.makeMove(context, "(4,8)", True)
        await self.makeMove(context, "(4,5)", True)
        await self.makeMove(context, "(3,7)", True)
        await self.makeMove(context, "(2,5)", True)
        await self.makeMove(context, "(4,6)", True)
        await self.makeMove(context, "(3,4)", True)
        assert self.board == checkpoint3, "Checkpoint 3: Failed to cancel out center pieces"

        await self.makeMove(context, "(5,7)", True)
        await self.makeMove(context, "(2,7)", True)
        await self.makeMove(context, "(4,7)", True)
        await self.makeMove(context, "(3,8)", True)
        await self.makeMove(context, "(8,9)", True)
        await self.makeMove(context, "(4,9)", True)
        await self.makeMove(context, "(8,8)", True)
        await self.makeMove(context, "(5,8)", True)
        await self.makeMove(context, "(7,7)", True)
        await self.makeMove(context, "(6,7)", True)
        await self.makeMove(context, "(8,6)", True)
        await self.makeMove(context, "(5,6)", True)
        await self.makeMove(context, "(9,6)", True)
        assert self.board == checkpoint4, "Checkpoint 4: Failed to cancel out center pieces"

        # SCORING
        assert self.player1LostStones == 2, "Player 1 lost stones incorrect!"
        assert self.player2LostStones == 13, "Player 2 lost stones incorrect!"
        assert self.endGame() == (20,-1.5), "Scoring is incorrect!"

        # RESET AND CONFIRM
        self.reset()
        assert self.board == endstate
    
    async def testSelfSurroundSuite(self, context):
        checkpoint1 = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,1,2,0,0,0,0],
            [0,0,1,0,1,0,0,0,0],
            [0,0,0,1,2,0,0,0,0],
            [0,0,0,2,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ]
        checkpoint2 = [
            [0,0,0,2,0,0,0,1,1],
            [0,0,2,0,2,0,0,1,1],
            [0,2,0,0,0,2,0,0,1],
            [0,0,2,0,2,0,0,0,0],
            [0,0,0,2,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ]

        await self.makeMove(context, "(4,6)", True)
        await self.makeMove(context, "(4,5)", True)
        await self.makeMove(context, "(5,7)", True)
        await self.makeMove(context, "(5,6)", True)
        await self.makeMove(context, "(4,8)", True)
        await self.makeMove(context, "(5,8)", True)
        await self.makeMove(context, "(3,7)", True)
        await self.makeMove(context, "(4,7)", True)
        assert self.board == checkpoint1, "Checkpoint 1: Failed to remove captured piece"

        await self.makeMove(context, "(9,9)", True)
        await self.makeMove(context, "(6,7)", True)
        await self.makeMove(context, "(8,9)", True)
        await self.makeMove(context, "(4,9)", True)
        await self.makeMove(context, "(9,8)", True)
        await self.makeMove(context, "(3,8)", True)
        await self.makeMove(context, "(8,8)", True)
        await self.makeMove(context, "(2,7)", True)
        await self.makeMove(context, "(9,7)", True)
        await self.makeMove(context, "(3,6)", True)
        await self.makeMove(context, "(4,7)", True)
        assert self.board == checkpoint2, "Checkpoint 2: Failed to have pieces self surround"

        # SCORING
        assert self.player1LostStones == 5, "Player 1 lost stones incorrect!"
        assert self.player2LostStones == 1, "Player 2 lost stones incorrect!"
        assert self.endGame() == (-5,11.5), "Scoring is incorrect!"

        # RESET AND CONFIRM
        self.reset()

    async def testKoSuite(self, context):
        checkpoint1 = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ]
        await self.makeMove(context, "(4,6)", True)
        await self.makeMove(context, "(6,6)", True)
        await self.makeMove(context, "(2,4)", True)

async def setup(bot):
    await bot.add_cog(GoMinigame(bot))