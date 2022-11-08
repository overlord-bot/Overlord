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
            link = result.find(href=True).get("href")
            page_data = requests.get(link)
            page_soup = BeautifulSoup(page_data.text, 'html.parser')

            score_board = page_soup.find("score-board")
            name = score_board.find('h1', class_="scoreboard__title").string.strip()
            percent = score_board.get("tomatometerscore")
            if len(percent) == 0:
                percent = "N/A"
            else:
                percent = f"{percent}%"
            audience = score_board.get("audiencescore")
            if len(audience) == 0:
                audience = "N/A"
            else:
                audience = f"{audience}%"
            await context.send(f"Name: {name} | URL: {link} | Tomatometer: {percent} | Audience Score: {audience}")
        else:
            await context.send("I couldn't find any results from that query. Try another one.")

async def setup(bot):
    await bot.add_cog(RottenTomatoesScraper(bot))
