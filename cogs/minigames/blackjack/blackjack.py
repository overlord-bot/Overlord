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
        self.dealercards = ""
        self.playercards = ""
        self.playercard1 = ""
        self.playercard2 = ""
        self.gamestart = False
        self.gameend = False
        self.splithand = False
        self.playerright = ""
        self.playerleft = ""
        self.rightscore = 0
        self.leftscore = 0
        self.rightdone = False
        self.leftdone = False
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
        "9": ":nine:","10":":keycap_ten:"}
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
            self.dealercards+=emojii[0]
            self.dealercards+=emojii[1]
            await context.send("Dealers cards are")
            await context.send(emojii[0] + emojii[1] + ":regional_indicator_x:")
            
            card1player = Blackjack.draw(self.cardsindeck)
            card2player = Blackjack.draw(self.cardsindeck)
            self.playercard1 = card1player
            self.playercard2 = card2player
            emojii1 = Blackjack.emoji(card1player)
            emojii2 = Blackjack.emoji(card2player)
            await context.send("Your cards are:")
            self.playercards+=emojii1[0]
            self.playercards+=emojii1[1]
            self.playercards+=emojii2[0]
            self.playercards+=emojii2[1]
            await context.send(emojii1[0]+emojii1[1] + emojii2[0] + emojii2[1])
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
                self.playercards = ""
                self.dealercards = ""
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
            if(self.splithand == False):
                self.playercards+=cardemoji[0]
                self.playercards+=cardemoji[1]
                self.playerscore+=cardscore
                #SHOW NEW HAND
                await context.send("Your current hand is")
                await context.send(self.playercards)
            elif(self.splithand == True):
                if(self.rightdone == False):
                    self.playerright+=cardemoji[0]
                    self.playerright+=cardemoji[1]
                    self.rightscore+=cardscore
                    await context.send("Your current hand to the right is")
                    await context.send(self.playerright)
                elif(self.leftdone == False):
                    self.playerleft+=cardemoji[0]
                    self.playerleft+=cardemoji[1]
                    self.leftscore+=cardscore
                    await context.send("Your current hand to the left is")
                    await context.send(self.playerleft)

            
            if(self.rightscore>21):
                await context.send("HAND TO RIGHT LOSE")
                self.rightdone = True
                self.rightscore = 0
                self.playerright = ""
                await context.send("Playing your hand to the left")
                await context.send(self.playerleft)
            if(self.leftscore>21):
                await context.send("HANDTOLEFTLOSE")
                self.gameend = True
                self.gamestart = False
                self.playerright = ""
                self.dealercards = ""
                self.splithand = False
                self.playerscore = 0
                self.dealerscore = 0
                self.rightscore = 0
                self.leftscore = 0
                self.rightdone = False
            elif(self.playerscore>21):
                await context.send("YOU LOSE")
                self.gameend = True
                self.gamestart = False
                self.playercards = ""
                self.dealercards = ""
                self.playerscore = 0
                self.dealerscore = 0
                self.rightscore = 0
                self.leftscore = 0
                self.rightdone = False
        else:
            await context.send("Please start a game first!")
        
    @commands.command()
    async def double(self, context):
        if(self.gamestart != True and self.gameend != False):
            await context.send("Please start a game first")
        else:
            await context.send("Doubling your bet")
        #need to implement betting before doing anything else here
        #can double on any hand that wasnt split
    @commands.command()
    async def split(self,context):
        if(self.gamestart != True and self.gameend != False):
            await context.send("Please start a game first")
        elif(self.playercard1[0]!=self.playercard2[0]):
            await context.send("You cannot split with this hand")
        elif(self.playercard1[0]==self.playercard2[0]):
            await context.send("Splitting hand")
            self.splithand = True
            self.playerscore = 0
            self.playerleft = Blackjack.emoji(self.playercard1)[0]
            self.playerleft += Blackjack.emoji(self.playercard1)[1]
            self.playerright = Blackjack.emoji(self.playercard2)[0]
            self.playerright += Blackjack.emoji(self.playercard2)[1]
            hand1card = Blackjack.draw(self.cardsindeck)
            hand2card = Blackjack.draw(self.cardsindeck)
            self.playerleft += Blackjack.emoji(hand1card)[0]
            self.playerleft += Blackjack.emoji(hand1card)[1]
            self.playerright += Blackjack.emoji(hand2card)[0]
            self.playerright += Blackjack.emoji(hand2card)[1]
            await context.send("Your hand to the left hand side is")
            await context.send(self.playerleft)
            await context.send("Your hand to the right hand side is")
            await context.send(self.playerright)
            await context.send("Playing your hand to the right")
            #Add implementation to actually play the hand later
            await context.send(self.playerright)
            cardscore = 0
            if(self.playercard2[0] == "J" or self.playercard2[0] == "K" or self.playercard2[0] == "Q"):
                cardscore = 10
            else:
                cardscore = int(re.search(r'\d+',self.playercard2).group())
            self.rightscore += cardscore
            cardscore2 = 0
            if(hand2card[0] == "J" or hand2card[0] == "K" or hand2card[0] == "Q"):
                cardscore2 = 10
            else:
                cardscore2 = int(re.search(r'\d+',hand2card).group())
            self.rightscore += cardscore2
            cardscore3 = 0
            if(self.playercard1[0] == "J" or self.playercard1[0] == "K" or self.playercard1[0] == "Q"):
                cardscore3 = 10
            else:
                cardscore3 = int(re.search(r'\d+',self.playercard1).group())
            self.leftscore += cardscore3
            cardscore4 = 0
            if(hand1card[0] == "J" or hand1card[0] == "K" or hand1card[0] == "Q"):
                cardscore4 = 10
            else:
                cardscore4 = int(re.search(r'\d+',hand1card).group())
            self.leftscore += cardscore4
    @commands.command()
    async def stand(self, context):
        """ Does not get another card switches to dealers turn """  # this is the description that will show up in !help
        #DEALER KEEPS ON HITTING UNTIL THEY HAVE A HIGHER NUMBER THAN THE PLAYER THEN THEY WIN
        #OUTPUT GAMES WINNER
        if(self.gamestart == True and self.gameend == False):
            dealercards1 = Blackjack.emoji(self.dealercard1)
            dealercards2 = Blackjack.emoji(self.dealercard2)
            self.dealercards+=dealercards2[0]
            self.dealercards+=dealercards2[1]
            originalscore = self.dealerscore
            originalhand = self.dealercards
            await context.send("dealer has the cards")
            await context.send(dealercards1[0]+dealercards1[1] + dealercards2[0] + dealercards2[1])
            if(self.splithand == True):
                if(self.rightdone == False):
                    self.playerscore = self.rightscore
                elif(self.leftdone == False):
                    self.playerscore = self.leftscore
                
            while(self.dealerscore <= self.playerscore):
                card = Blackjack.draw(self.cardsindeck)
                if(card[0] == "J" or card[0] == "K" or card[0] == "Q"):
                    cardscore = 10
                else:
                    cardscore = int(re.search(r'\d+',card).group())
                dealeremoji = Blackjack.emoji(card)
                self.dealercards+=dealeremoji[0]
                self.dealercards+=dealeremoji[1]
                await context.send("Dealer drew")
                await context.send(dealeremoji[0] + dealeremoji[1])
                self.dealerscore+=cardscore
                await context.send("Dealer's current hand is")
                await context.send(self.dealercards)
            if(self.splithand == False):
                if(self.dealerscore > 21):
                    await context.send("YOU WIN")
                    self.gameend = True
                    self.gamestart = False
                    self.playercards = ""
                    self.dealercards = ""
                    
                elif(self.dealerscore > self.playerscore):
                    await context.send("YOU LOSE")
                    self.gameend = True
                    self.gamestart = False
                    self.playercards = ""
                    self.dealercards = ""
                else:
                    await context.send("YOU WIN")
                    self.gameend = True
                    self.gamestart = False
                    self.playercards = ""
                    self.dealercards = ""
            elif(self.splithand == True):
                if(self.dealerscore > 21):
                    if(self.rightdone == False):
                        await context.send("YOU WIN ON RIGHT HAND")
                        self.rightdone = True
                        self.rightscore = 0
                        self.playerright = ""
                        self.dealerscore = originalscore
                        self.dealercards = originalhand
                        await context.send("Playing your hand to the left")
                        await context.send(self.playerleft)
                    elif(self.leftdone == False):
                        await context.send("YOU WIN ON LEFT HAND")
                        self.gameend = True
                        self.gamestart = False
                        self.playerright = ""
                        self.dealercards = ""
                        self.splithand = False
                        self.playerscore = 0
                        self.dealerscore = 0
                        self.rightscore = 0
                        self.leftscore = 0
                        self.rightdone = False
                elif(self.dealerscore > self.playerscore):
                    if(self.rightdone == False):
                        await context.send("YOU LOSE ON RIGHT HAND")
                        self.rightdone = True
                        self.rightscore = 0
                        self.playerright = ""
                        self.dealerscore = originalscore
                        self.dealercards = originalhand
                        await context.send("Playing your hand to the left")
                        await context.send(self.playerleft)
                    elif(self.leftdone == False):
                        await context.send("YOU LOSE ON LEFT HAND")
                        self.gameend = True
                        self.gamestart = False
                        self.playerright = ""
                        self.dealercards = ""
                        self.splithand = False
                        self.playerscore = 0
                        self.dealerscore = 0
                        self.rightscore = 0
                        self.leftscore = 0
                        self.rightdone = False
                elif(self.playerscore > self.dealerscore):
                    if(self.rightdone == False):
                        await context.send("YOU WIN ON RIGHT HAND")
                        self.rightdone = True
                        self.rightscore = 0
                        self.playerright = ""
                        self.dealerscore = originalscore
                        self.dealercards = originalhand
                        await context.send("Playing your hand to the left")
                        await context.send(self.playerleft)
                    elif(self.leftdone == False):
                        await context.send("YOU WIN ON LEFT HAND")
                        self.gameend = True
                        self.gamestart = False
                        self.playerright = ""
                        self.dealercards = ""
                        self.splithand = False
                        self.playerscore = 0
                        self.dealerscore = 0
                        self.rightscore = 0
                        self.leftscore = 0
                        self.rightdone = False
        else:
            await context.send("Please start a game first!")
    
async def setup(bot):
    await bot.add_cog(Blackjack(bot))
