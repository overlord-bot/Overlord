#allow user to get facts about certain characters from the overlord series
#by using the command !overlordfacts <character>
#sends a link to the overlord wiki page for that character

import discord
from discord.ext import commands
import random

class OverlordFacts(commands.Cog, name="Overlord Facts"):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="overlordfacts",
        help="Get facts about a character from the Overlord series! Usage: !overlordfacts <character>"
    )
    async def overlordfacts(self, context, character: str):
        """Sends the wiki link of the specified Overlord Character."""
        character = character.title().replace(" ", "_")
        await context.send("https://overlordmaruyama.fandom.com/wiki/" + character)

async def setup(bot):
    await bot.add_cog(OverlordFacts(bot))
