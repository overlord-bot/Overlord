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

        search_data = requests.get(url)
        search_soup = BeautifulSoup(search_data.text, 'html.parser')

        anime_url = search_soup.find("a", {"class": "hoverinfo_trigger"}).get("href")

        print(anime_url)

        anime_data = requests.get(anime_url)
        anime_soup = BeautifulSoup(anime_data.text, 'html.parser')
        score = anime_soup.find("div", {"class": "score-label"}).get_text()
        description = anime_soup.find("p", {"itemprop": "description"}).get_text()
        ranking = anime_soup.find("span", {"class": "numbers ranked"}).get_text()
        popularity = anime_soup.find("span", {"class": "numbers popularity"}).get_text()

        await context.send(f"URL: {anime_url} | Score: {score}/10 | {ranking} | {popularity} \n\nDescription: \n{description}")


async def setup(bot):
    await bot.add_cog(AnimeScraper(bot))
