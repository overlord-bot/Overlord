#Rotten Tomatoes scraper
import requests
from bs4 import BeautifulSoup

import discord
from discord.ext import commands

class RottenTomatoesScraper(commands.Cog, name="Rotten Tomatoes Scraper"):
    """Scrapes Rotten Tomatoes"""

    def __init__(self, bot):
        self.bot = bot


    def findMedia(self, soup, year):
        results = soup.findAll("search-page-media-row")

        for item in results:
            releaseyear = item["releaseyear"].strip()
            print(f"{releaseyear}")
            if year == releaseyear:
                return item
        return None

    @commands.command()
    async def tomato(self, context, *args):
        """
        tomato <name> <type> <year>
        Finds media from rotten tomatoes and displays it's critical score and audience score
        <name>: Name of the media. If it has multiple words it must be in quotes!
        <type>: Type of the media. Either can be tv or movie
        <year>: The year that the movie came out in
        """
        name = args[0].strip()
        mediaType = None
        year = None
        if len(args) > 1:
            if args[1] == "tv" or args[1] == "movie":
                mediaType = args[1]
            else:
                await context.send("I couldn't recognize that media type! Try 'tv' or 'movie'")
        if len(args) > 2:
            if args[2].isnumeric() and int(args[2]) > 0:
                year = args[2]
            else:
                await context.send("I couldn't recognize what year that was! Try typing in a positive integer")

        url = "https://www.rottentomatoes.com/search?search=" + name.replace(" ", "%20")
        print(f"Url of search result page: {url}")
        search_data = requests.get(url)
        result = None

        soup = BeautifulSoup(search_data.text, 'html.parser')
        if mediaType:
            if year is None:
                result = soup.find('search-page-result', type=mediaType).find('search-page-media-row')
            else:
                parent = soup.find('search-page-result', type=mediaType)
                result = self.findMedia(parent, year)
        else:
            if year is None:
                result = soup.find('search-page-media-row')
            else:
                parent = soup.find('search-page-result')
                result = self.findMedia(parent, year)
            mediaType = result.find_parent("search-page-result")["type"]

        if result is not None:
            link = result.find(href=True).get("href")
            page_data = requests.get(link)
            page_soup = BeautifulSoup(page_data.text, 'html.parser')
            
            percent = "N/A"
            audience = "N/A"
            if mediaType == "movie":
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
            
            elif mediaType == "tv":
                score_board = page_soup.find("section", class_="tv-series__scoreboard score-panel-wrap")
                name = score_board.find('h1', class_="mop-ratings-wrap__title mop-ratings-wrap__title--top").string.strip()
                percent = score_board.find('div', class_="mop-ratings-wrap__half critic-score").find("span", class_="mop-ratings-wrap__percentage")
                if percent is None:
                    percent = "N/A"
                else:
                    percent = percent.string.strip()
                    percent = f"{percent}"
                audience = score_board.find('div', class_="mop-ratings-wrap__half audience-score").find("span", class_="mop-ratings-wrap__percentage")
                if audience is None:
                    audience = "N/A"
                else:
                    audience = audience.string.strip()
                    audience = f"{audience}"

            await context.send(f"Name: {name}\nURL: {link}\nTomatometer: {percent}\nAudience Score: {audience}")
        else:
            await context.send("I couldn't find any results from that query. Try another one.")

async def setup(bot):
    await bot.add_cog(RottenTomatoesScraper(bot))
