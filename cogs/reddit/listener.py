import requests
from bs4 import BeautifulSoup

import discord
from discord.ext import commands


class RedditListener(commands.Cog, name="Reddit Listener"):
    """Listens for a new reddit post"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def redditlisten(self, context, subreddit):
        print(context)
        await context.reply("Testing")

    #await context.reply("Your file is:", file=discord.File(file, "list_of_commits.txt"))

async def setup(bot):
    await bot.add_cog(RedditListener(bot))
