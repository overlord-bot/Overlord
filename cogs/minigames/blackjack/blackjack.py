# Blackjack
#Author: Christian Stec
from discord.ext import commands
import random
import re
class Blackjack(commands.Cog, name="Blackjack"):
    """Blackjack Game"""

    def __init__(self, bot):
        self.bot = bot
        self.playerscore = 0
        self.dealerscore = 0
        self.dealercard1 = ""
        self.dealercard2 = ""
        self.cardsindeck = []
        self.gamestart = False
        self.gameend = False
    def draw(deck):
        draw = random.randint(0,len(deck))
        card = deck[draw]
        deck.remove(card)
        return card
    def points(card1,card2):
        card1score = 0
        card2score = 0
        totalscore = 0
        if(card1[0] == "J" or card1[0] == "K" or card1[0] == "Q"):
            card1score = 10
        else:
            card1score = int(re.search(r'\d+',card1).group())
        if(card2[0] == "J" or card2[0] == "K" or card2[0] == "Q"):
            card2score = 10
        else:
            card2score = int(re.search(r'\d+',card2).group())
        #check for blackjack
        if(card1 == 10 and card2 == 1):
            totalscore = 21
        if(card1 == 1 and card2 == 10):
            totalscore = 21
        else:
            totalscore = card1score + card2score
        return totalscore

    def emoji(card):
        emoji1 = ""
        emoji2 = ""
        emojinumbers = {"J": ":regional_indicator_j:","K": ":regional_indicator_k:","Q": ":regional_indicator_q:",
        "1": ":one:","2":":two:","3":":three:","4":":four:","5":":five:","6":":six:","7":":seven:","8":":eight:",
        "9": ":nine","10":":keycap_ten:"}
        emojisuites = {"H": ":hearts:","C": ":clubs:","S": ":spades:","D": ":diamonds:"}
        if(card[0] == "J" or card[0] == "K" or card[0] == "Q"):
                emoji1 = emojinumbers[card[0]]
                emoji2 = emojisuites[card[1]]
        else:
            cardscore = int(re.search(r'\d+',card).group())
            if(cardscore == 10):
                emoji1 = emojinumbers[str(cardscore)]
                emoji2 = emojisuites[card[2]]
            else:
                emoji1 = emojinumbers[str(cardscore)]
                emoji2 = emojisuites[card[1]]
        emojis = [emoji1,emoji2]
        return emojis




    @commands.command()
    async def blackjack(self, context):
        """Play the casino game blackjack"""  # this is the description that will show up in !help
        if(self.gamestart == True):
           await context.send("Please finish the current game you are in!")
        else:
            self.gamestart = True
            self.gameend = False
            self.cardsindeck = ["1H","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","1C","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC",
        "1S","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","1D","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD"]
            random.shuffle(self.cardsindeck)
            card1dealer = Blackjack.draw(self.cardsindeck)
            hiddencarddealer = Blackjack.draw(self.cardsindeck)
            self.dealercard1 = card1dealer
            self.dealercard2 = hiddencarddealer
            emojii = Blackjack.emoji(card1dealer)
            await context.send("Dealers cards are")
            await context.send(emojii[0] + emojii[1] + ":heavy_plus_sign:" + ":regional_indicator_x:")
            
            card1player = Blackjack.draw(self.cardsindeck)
            card2player = Blackjack.draw(self.cardsindeck)
            emojii1 = Blackjack.emoji(card1player)
            emojii2 = Blackjack.emoji(card2player)
            await context.send("Your cards are:")
            await context.send(emojii1[0]+emojii1[1] + ":heavy_plus_sign:" + emojii2[0] + emojii2[1])
            self.dealerscore = Blackjack.points(card1dealer,hiddencarddealer)
            self.playerscore = Blackjack.points(card1player,card2player)
            #check to see if the game ends when a player or dealer gets a blackjack
            dealerblackjack = False
            playerblackjack = False
            #Check if either the player or the dealer has blackjack
            if(self.dealerscore == 21):
                await context.send("DEALER HAS BLACKJACK!")
                dealerblackjack = True
            if(self.playerscore == 21):
                await context.send("PLAYER HAS BLACKJACK")
                playerblackjack = True
            if(playerblackjack == True or dealerblackjack == True):
                self.gameend = True
                self.gamestart = False
                #reset deck
                self.cardsindeck = ["1H","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","1C","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC",
            "1S","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","1D","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD"]
                #EXIT PROGRAM
    @commands.command()
    async def hit(self, context):
        """ Gets another card """  # this is the description that will show up in !help
        if(self.gamestart == True and self.gameend == False):
            card = Blackjack.draw(self.cardsindeck)
            if(card[0] == "J" or card[0] == "K" or card[0] == "Q"):
                cardscore = 10
            else:
                cardscore = int(re.search(r'\d+',card).group())
            cardemoji = Blackjack.emoji(card)
            await context.send("You drew")
            await context.send(cardemoji[0]+cardemoji[1])
            self.playerscore+=cardscore
            if(self.playerscore>21):
                await context.send("YOU LOSE")
                self.gameend = True
                self.gamestart = False
        else:
            await context.send("Please start a game first!")
        
        
    @commands.command()
    async def stand(self, context):
        """ Does not get another card switches to dealers turn """  # this is the description that will show up in !help
        #DEALER KEEPS ON HITTING UNTIL THEY HAVE A HIGHER NUMBER THAN THE PLAYER THEN THEY WIN
        #OUTPUT GAMES WINNER
        if(self.gamestart == True and self.gameend == False):
            dealercards1 = Blackjack.emoji(self.dealercard1)
            dealercards2 = Blackjack.emoji(self.dealercard2)
            await context.send("dealer has the cards")
            await context.send(dealercards1[0]+dealercards1[1] + ":heavy_plus_sign:" + dealercards2[0] + dealercards2[1])

            while(self.dealerscore <= self.playerscore):
                card = Blackjack.draw(self.cardsindeck)
                if(card[0] == "J" or card[0] == "K" or card[0] == "Q"):
                    cardscore = 10
                else:
                    cardscore = int(re.search(r'\d+',card).group())
                dealeremoji = Blackjack.emoji(card)
                await context.send("Dealer drew")
                await context.send(dealeremoji[0] + dealeremoji[1])
                self.dealerscore+=cardscore
            if(self.dealerscore > 21):
                await context.send("YOU WIN")
                self.gameend = True
                self.gamestart = False
            if(self.dealerscore > self.playerscore):
                await context.send("YOU LOSE")
                self.gameend = True
                self.gamestart = False
            else:
                await context.send("YOUWIN")
                self.gameend = True
                self.gamestart = False
        else:
            await context.send("Please start a game first!")
    
async def setup(bot):
    await bot.add_cog(Blackjack(bot))
