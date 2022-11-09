# MyAnimeList.net scraper
import asyncio

import requests
from bs4 import BeautifulSoup

from discord.ext import commands

from cogs.moderation.virus_scanner import scan_link
import os

from dotenv import load_dotenv
import vt


class AnimeScraper(commands.Cog, name="Anime Scraper"):
    """Scrapes MyAnimeList.net"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def anime(self, context, *search):
        """Searches for an anime"""  # this is the description that will show up in !help

        url = "https://myanimelist.net/search/all?q=" + '%20'.join(search) + "&cat=all"
        print(f"Url of search result page: {url}")

        # link_is_safe = scan_link(url)
        link_is_safe = True

        if link_is_safe:
            search_data = requests.get(url)
            search_soup = BeautifulSoup(search_data.text, 'html.parser')

            anime_url = search_soup.find("a", {"class": "hoverinfo_trigger"}).get("href")
            print(f"Url of first anime result: {anime_url}")

            # Gets data from the first search result's page
            anime_data = requests.get(anime_url)
            anime_soup = BeautifulSoup(anime_data.text, 'html.parser')

            # .find ("element type", {"class": "class of target element"{).get_text()
            score = anime_soup.find("div", {"class": "score-label"}).get_text()
            description = anime_soup.find("p", {"itemprop": "description"}).get_text()
            ranking = anime_soup.find("span", {"class": "numbers ranked"}).get_text()
            popularity = anime_soup.find("span", {"class": "numbers popularity"}).get_text()

            await context.send(f"URL: {anime_url}"
                               f"\nScore: {score}/10 | {ranking} | {popularity}"
                               f"\n\nDescription: \n{description}")
        else:
            await context.send(f"Failed")


async def setup(bot):
    await bot.add_cog(AnimeScraper(bot))
