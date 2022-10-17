# Clone of the game wordle

from discord.ext import commands
import emoji
import random
import os
class WordGame(commands.Cog, name="Word Game"):
    """Plays the word game that is similar to Wordle"""
    """words.txt from https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt"""

    def __init__(self, bot):
        self.bot = bot
        self.word_list = self.get_words()
        self.current_word = ''
        self.round = -1
        self.current_progress = []
        self.emojidict = {"G": ":green_square:",
                          "Y": ":yellow_square:",
                          "B": ":black_large_square:",}
        self.max_round = -1

    def get_words(self):
        """From https://github.com/charlesreid1/five-letter-words/blob/master/get_words.py"""

        # Load the file.
        with open(os.path.join(os.getcwd(), "cogs", "minigames", "words.txt"),'r') as f:
            # This drops the \n at the end of each line:
            words = f.read().splitlines()

        return words

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
                       return_status = return_status + self.current_progress[i][0] + ": " + ''.join(self.current_progress[i][1]) + '\n'
        return return_status

    def to_emoji(self, message):
        """Replaces letters with emoji names"""
        new_message = message.replace('G', self.emojidict['G']).replace('Y', self.emojidict['Y']).replace('B', self.emojidict['B'])
        return new_message

    def clear_game(self):
        """Clears game state"""
        self.round = -1
        self.max_round = -1
        self.current_word = ''
        self.current_progress = []

    """
    @commands.command()
    async def getword(self, ctx):
        #Returns the test word. FOR DEBUG ONLY!
        await ctx.send(self.current_word)
    """

    @commands.command()
    async def wordgame(self, ctx, rounds: int = -1):
        """Starts the word game. 
        rounds: an optional number of rounds to play the game with."""
        if (self.round >= 0):
            await ctx.send("The Word Game has already started!")
        else:
            self.round = 0
            self.current_word = random.choice(self.word_list)
            if (rounds >= 1):
                self.max_round = rounds
                await ctx.send("Word Game started with " + str(self.max_round) + " rounds!")
            else:
                await ctx.send("Word Game started!")
    
    @wordgame.error
    async def wordgame_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("I couldn't read how many rounds that was! Try typing an integer number.")
    
    @commands.command()
    async def addword(self, ctx, word: to_lower):
        """Add 5-lettered word to list of words"""
        if(self.round >= 0):
            if(word in self.word_list):
                self.round += 1
                wordlist = self.checkword(word, self.current_word)
                self.current_progress.append((word, wordlist))
                emojimessage = self.to_emoji(''.join(wordlist))
                await ctx.send(emoji.emojize(emojimessage))
                if (wordlist.count('G') == len(self.current_word)):
                    self.clear_game()
                    await ctx.send("You win!")
                    return
                
                if(self.round >= self.max_round and self.max_round != -1):
                    await ctx.send("Word Game ended! The word was " + self.current_word)
                    self.clear_game()
            else:
                await ctx.send("It seems that word is not in my dictionary. Try typing another 5-lettered word.")
        else:
            await ctx.send("The Word Game has not started!")

    @addword.error
    async def addword_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Your addword is missing a word!")

    @commands.command()
    async def endwordgame(self, ctx):
        """Ends the word game if not started"""
        if (self.round >= 0):
            await ctx.send("Word Game ended! The word was " + self.current_word)
            self.clear_game()
        else:
            await ctx.send("The Word Game has not started!")

    @commands.command()
    async def checkstatus(self, ctx):
        """Check the current game status"""
        if (self.round > 0):
            return_text = self.print_status()
            emoji_text = self.to_emoji(return_text)
            await ctx.send(emoji.emojize(emoji_text))
        elif (self.round == 0):
             await ctx.send("No one has added any words!")
        else:
            await ctx.send("The Word Game has not started!")


async def setup(bot):
    await bot.add_cog(WordGame(bot))