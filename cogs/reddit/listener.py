import urllib.request #python3 bot.py -fast -load reddit
import json

import discord
from discord.ext import commands

import threading #https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds



class RedditListener(commands.Cog, name="Reddit Listener"):
    """Listens for a new reddit post"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def redditlisten(self, context, subreddit):
        reddit_data = getRedditData(subreddit)
        newest_post = reddit_data["data"]["children"][3]["data"]["name"]
        new_posts = getNewPosts(context, reddit_data, newest_post)
        #print(new_posts)
        
        await sendPosts(context, new_posts)

    #await context.reply("Your file is:", file=discord.File(file, "list_of_commits.txt"))

def getRedditData(subreddit): #https://www.reddit.com/r/rpi/new.json?sort=new
    url = "https://www.reddit.com/r/" + subreddit + "/new.json?sort=new"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    #posts = data["data"]["children"] 
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
    await bot.add_cog(RedditListener(bot))
