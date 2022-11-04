from hashlib import new
import urllib.request #python3 bot.py -fast -load reddit
import requests
#from urllib.request import Request, urlopen
import json

import discord
from discord.ext import commands

from threading import Event, Thread
#https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds


class NewRedditPosts(commands.Cog, name="Newest Reddit Post Retriever"):
    """Get new reddit posts"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newpost(self, context, subreddit, amount = 1):
        print(amount)
        reddit_data = getRedditData(subreddit)
        newest_post = reddit_data["data"]["children"][int(amount)]["data"]["name"]

        new_posts = getNewPosts(context, reddit_data, newest_post)

        
        await sendPosts(context, new_posts)

    #await context.reply("Your file is:", file=discord.File(file, "list_of_commits.txt"))


def getRedditData(subreddit): #https://www.reddit.com/r/rpi/new.json?sort=new
    url = "https://www.reddit.com/r/" + subreddit + "/new.json?sort=new"
    response = requests.get(url, headers = {'User-agent': 'your bot 0.1'}).text
    data = json.loads(response) #.decode('utf-8')
    return data

def getNewPosts(context, data, new_post):
    new_posts = []
    posts = data["data"]["children"] 
    for num_post in range(len(posts)):
        post = posts[num_post]["data"]
        if post["name"] == new_post:
            return new_posts
        new_posts.append(post)
    return new_posts


async def sendPosts(context, new_posts):
    for num_post in range(len(new_posts)):
        post = new_posts[num_post]
        embedMessage = getEmbedMessage(post)
        await context.send(embed=embedMessage)

def getEmbedMessage(post):
    embed=discord.Embed(title=post["title"], url="https://www.reddit.com" + post["permalink"], color=discord.Color.blue())
    return embed
        
    
async def setup(bot):
    await bot.add_cog(NewRedditPosts(bot))
