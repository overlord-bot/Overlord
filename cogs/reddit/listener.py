from hashlib import new
import requests
import json

import discord
from discord.ext import commands

import asyncio
import functools
import typing
import time


class RedditListener(commands.Cog, name="Reddit Listener"):
    """Listens for a new reddit post"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def redditlisten(self, context, subreddit, min_time = "5"):
        await context.send("Starting listen for the subreddit '" + subreddit + "' for " + min_time + " minutes")

        reddit_data = getRedditData(subreddit)

        #Find newest post
        newest_post = reddit_data["data"]["children"][1]["data"]["name"]

        #Run for min_time minutes
        t_end = time.time() + 60 * int(min_time)
        while time.time() < t_end:
            await blocking_func(5) #sleep that doesn't break discord
            newest_post = await runPostCheck(context, subreddit, newest_post)

        await context.send("Completed listen")

async def runPostCheck(context, subreddit, newest_post):
    reddit_data = getRedditData(subreddit)
    new_post = reddit_data["data"]["children"][0]["data"]["name"]
    #print("Checking new: " + new_post + " against newest: " + str(newest_post))
    
    #Check if new post is found
    if new_post == newest_post:
        return new_post
    #print("is a new post")

    #Send new post
    new_posts = getNewPosts(context, reddit_data, newest_post)
    await sendPosts(context, new_posts)
    return new_post


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

@to_thread
def blocking_func(interval):
    time.sleep(interval)
    return "some stuff"


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
    await bot.add_cog(RedditListener(bot))
