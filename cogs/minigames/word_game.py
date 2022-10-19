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
        self.emojidict = {"G": ":green_square:",
                          "Y": ":yellow_square:",
                          "B": ":black_large_square:",}
        self.player_dict = dict()

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

    def print_status(self, user_id):
        """Returns the current status of the for the user that called the command"""
        return_status = str()
        current_progress = self.player_dict[user_id]["progress"]
        for i in range(0, len(current_progress)):
                       return_status = return_status + current_progress[i][0] + ": " + ''.join(current_progress[i][1]) + '\n'
        return return_status

    def to_emoji(self, message):
        """Replaces letters with emoji names"""
        new_message = message.replace('G', self.emojidict['G']).replace('Y', self.emojidict['Y']).replace('B', self.emojidict['B'])
        return new_message

    def clear_game(self, user_id):
        """Clears game state"""
        self.player_dict.pop(user_id)

    
    @commands.command()
    async def getword(self, ctx):
        #Returns the test word. FOR DEBUG ONLY!
        await ctx.send(self.player_dict[ctx.author.id]["word"])
    

    @commands.command()
    async def wordgame(self, ctx, rounds: int = -1):
        """Starts the word game for the user. 
        rounds: an optional number of rounds to play the game with."""
        if (ctx.author.id in self.player_dict.keys()):
            await ctx.send("The Word Game has already started!")
        else:
            current_word = random.choice(self.word_list)
            current_dict = {"word": current_word, "progress" : [], "rounds" : 0, "max_round" : -1}
            self.player_dict[ctx.author.id] = current_dict
            if (rounds >= 1):
                current_dict["max_round"] = rounds
                await ctx.send("Word Game started with " + str(current_dict["max_round"]) + " rounds!")
            else:
                await ctx.send("Word Game started!")
    
    @wordgame.error
    async def wordgame_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("I couldn't read how many rounds that was! Try typing an integer number.")
    
    @commands.command()
    async def addword(self, ctx, word: to_lower):
        """Add 5-lettered word to list of words"""
        if(ctx.author.id in self.player_dict.keys()):
            current_dict = self.player_dict[ctx.author.id]
            if(word in self.word_list):
                current_dict["rounds"] += 1
                wordlist = self.checkword(word, current_dict["word"])
                current_dict["progress"].append((word, wordlist))
                emojimessage = self.to_emoji(''.join(wordlist))
                await ctx.send(emoji.emojize(emojimessage))
                if (wordlist.count('G') == len(current_dict["word"])):
                    self.clear_game(ctx.author.id)
                    await ctx.send("You win!")
                    return
                
                if(current_dict["rounds"] >= current_dict["max_round"] and current_dict["max_round"] != -1):
                    await ctx.send("Word Game ended! The word was " + current_dict["word"])
                    self.clear_game(ctx.author.id)
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
        """Ends the word game for the user if not started"""
        if (ctx.author.id in self.player_dict.keys()):
            await ctx.send("Word Game ended! The word was " + self.player_dict[ctx.author.id]["word"])
            self.clear_game(ctx.author.id)
        else:
            await ctx.send("The Word Game has not started!")

    @commands.command()
    async def checkstatus(self, ctx):
        """Check the current game status for the user"""
        if (ctx.author.id in self.player_dict.keys()):
            current_dict = self.player_dict[ctx.author.id]
            if (current_dict["rounds"] > 0):
                return_text = self.print_status(ctx.author.id)
                emoji_text = self.to_emoji(return_text)
                await ctx.send(emoji.emojize(emoji_text))
            
            elif (current_dict["rounds"] == 0):
                 await ctx.send("No one has added any words!")
        else:
            await ctx.send("The Word Game has not started!")

async def setup(bot):
    await bot.add_cog(WordGame(bot))