#Rotten Tomatoes scraper
import requests
from bs4 import BeautifulSoup

import discord
from discord.ext import commands

class RottenTomatoesScraper(commands.Cog, name="Rotten Tomatoes Scraper"):
    """Scrapes Rotten Tomatoes"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tomato(self, context, *args):
        url = "https://www.rottentomatoes.com/search?search=" + "%20".join(args)
        print(f"Url of search result page: {url}")
        search_data = requests.get(url)
        
        soup = BeautifulSoup(search_data.text, 'html.parser')
        result = soup.find('search-page-media-row')

        if result is not None:
            name = result.find(slot="title")
            print("Printing name:" + name.string.strip())

async def setup(bot):
    await bot.add_cog(RottenTomatoesScraper(bot))
