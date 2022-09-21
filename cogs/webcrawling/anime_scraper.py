# MyAnimeList.net scraper
import requests
from bs4 import BeautifulSoup

from discord.ext import commands


class AnimeScraper(commands.Cog, name="Anime Scraper"):
    """Scrapes MyAnimeList.net"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def anime(self, context, search: str):
        """Searches for an anime"""  # this is the description that will show up in !help
        url = "https://myanimelist.net/search/all?q=" + search + "&cat=all"

        data = requests.get(url)
        html = BeautifulSoup(data.text, 'html.parser')

        a_href = html.find("a", {"class": "hoverinfo_trigger"}).get("href")
        await context.send(a_href)


async def setup(bot):
    await bot.add_cog(AnimeScraper(bot))
