from discord.ext import commands
from bs4 import BeautifulSoup

dining_halls = {"!commons": "https://everyday.dynamify.com/store/17881",
              "!sage": "https://everyday.dynamify.com/store/18025",
              "!blitman": "https://everyday.dynamify.com/store/18031",
              "!barh": "https://everyday.dynamify.com/store/18026",
              }
              

class MenuScraper(commands.Cog, name="Menu Scraper"):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self, message):

        msg = message.content.lower()

        # reacts with a specified emoji
        if msg in dining_halls.keys():
            await message.reply(dining_halls[msg])


   


async def setup(bot):
    await bot.add_cog(MenuScraper(bot))
