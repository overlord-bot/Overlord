# Clone of the game wordle

from discord.ext import commands
import emoji


class WordGame(commands.Cog, name="Word Game"):
    """Plays the word game that is similar to Wordle"""

    def __init__(self, bot):
        self.bot = bot
        self.word = "jeans"
        self.round = -1
        self.current_progress = []
        self.emojidict = {"G": ":green_square:",
                          "Y": ":yellow_square:",
                          "B": ":black_large_square:",
                          }
    def to_lower(arg):
        """Helper function"""
        return arg.lower()

    def checkword(self, word, checked_word):
        """Compare current word to checked word"""
        """Requires that word and checked_word are same case and of same length"""

        currentlist = []
        letterdict = dict()
        for i in range(0, len(checked_word)):
            currentlet = checked_word[i]
            if currentlet in letterdict.keys():
                letterdict[currentlet] += 1
            else:
                letterdict[currentlet] = 1

        for i in range(0, len(word)):
            currentlet = word[i]
            comparedlet = checked_word[i]

            if currentlet == comparedlet:
                currentlist.append("G")
                letterdict[currentlet] -= 1
            else:
                if currentlet in checked_word and letterdict[currentlet] > 0:
                    currentlist.append("Y")
                    letterdict[currentlet] -= 1
                else:
                    currentlist.append("B")
        
        return currentlist

    def print_status(self):
        """Returns the current status of the game"""
        return_status = str()
        for i in range(0, len(self.current_progress)):
                       return_status = return_status + ''.join(self.current_progress[i]) + '\n'
        return return_status

    def to_emoji(self, message):
        """Replaces letters with emoji names"""
        new_message = message.replace('G', self.emojidict['G']).replace('Y', self.emojidict['Y']).replace('B', self.emojidict['B'])
        return new_message

    @commands.command()
    async def getword(self, ctx):
        """Returns the test word. FOR DEBUG ONLY!"""
        await ctx.send(self.word)


    @commands.command()
    async def start_game(self, ctx):
        """Starts the word game."""
        if (self.round >= 0):
            await ctx.send("Game already started!")
        else:
            self.round = 0
            # TODO: Add multiple words
            await ctx.send("Game Started!")

    @commands.command()
    async def add_word(self, ctx, word: to_lower):
        """Add word to list of words"""
        if(self.round >= 0):
            if(len(word) == len(self.word)):
                self.round += 1
                wordlist = self.checkword(word, self.word)
                self.current_progress.append(wordlist)
                emojimessage = self.to_emoji(''.join(wordlist))
                await ctx.send(emoji.emojize(emojimessage))
                if (wordlist.count('G') == len(self.word)):
                    self.round = -1
                    self.current_progress = []
                    await ctx.send("You win!")
            else:
                await ctx.send("Argument not correct length!")
        else:
            await ctx.send("The game has not started!")

    @add_word.error
    async def add_word_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Not enough arguments!")

    @commands.command()
    async def end_game(self, ctx):
        """Ends the word game if not started"""
        if (self.round >= 0):
            self.round = -1
            self.current_progress = []
            await ctx.send("Game ended! The word was " + self.word)
        else:
            await ctx.send("The game hasn't started!")

    @commands.command()
    async def check_status(self, ctx):
        """Check the current game status"""
        if (self.round > 0):
            return_text = self.print_status()
            await ctx.send(return_text)
        elif (self.round == 0):
             await ctx.send("No one has added any words!")
        else:
            await ctx.send("The game has not started!")


async def setup(bot):
    await bot.add_cog(WordGame(bot))