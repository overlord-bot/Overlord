# Blackjack
#Author: Christian Stec
from discord.ext import commands
import random
import re
class Minigames(commands.Cog, name="Minigames"):
    """Minigames to play"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blackjack(self, context):
        """Play the casino game blackjack"""  # this is the description that will show up in !help
    #list of deck of  cards
        cardsindeck = ["1H","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","1C","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC",
        "1S","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","1D","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD"]
    #randomize the list like shuffling a deck
        random.shuffle(cardsindeck)
        draw = random.randint(0,51)
        card1dealer = cardsindeck[draw]
        cardsindeck.remove(card1dealer)
        draw2 = random.randint(0,50)
        hiddencarddealer = cardsindeck[draw2]
        cardsindeck.remove(hiddencarddealer)
        await context.send("Dealers cards are: " + card1dealer + " X")
        draw3 = random.randint(0,49)
        card1player = cardsindeck[draw3]
        cardsindeck.remove(card1player)
        draw4 = random.randint(0,48)
        card2player = cardsindeck[draw4]
        cardsindeck.remove(card2player)
        await context.send("Your cards are: " + card1player + " " + card2player)
        dealercard1score = 0
        dealercard2score = 0
        dealertotalscore = 0
        playercard1score = 0
        playercard2score = 0
        playertotalscore = 0
        #Convert Jokers, Queens, Kings to their numerical value of 10
        if(card1dealer[0] == "J" or card1dealer[0] == "K" or card1dealer[0] == "Q"):
            dealercard1score = 10
        else:
            dealercard1score = int(re.search(r'\d+',card1dealer).group())
        if(hiddencarddealer[0] == "J" or hiddencarddealer[0] == "K" or hiddencarddealer[0] == "Q"):
            dealercard2score = 10
        else:
            dealercard2score = int(re.search(r'\d+',hiddencarddealer).group())
        if(card1player[0] == "J" or card1player[0] == "K" or card1player[0] == "Q"):
            playercard1score = 10
        else:
            playercard1score = int(re.search(r'\d+',card1player).group())
        if(card2player[0] == "J" or card2player[0] == "K" or card2player[0] == "Q"):
            playercard2score = 10
        else:
            playercard2score = int(re.search(r'\d+',card2player).group())
        playertotalscore = playercard1score + playercard2score
        dealertotalscore = dealercard1score + dealercard2score
        await context.send("Dealerscore: " + str(dealertotalscore))
        await context.send("Playerscore: " + str(playertotalscore))
        #while (keep hitting until user stands)

        #output who wins the game
        #await context.send("")


async def setup(bot):
    await bot.add_cog(Minigames(bot))