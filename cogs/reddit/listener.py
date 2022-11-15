from hashlib import new
import urllib.request #python3 bot.py -fast -load reddit
import requests
#from urllib.request import Request, urlopen
import json

import discord
from discord.ext import commands

import datetime

import asyncio
import functools
import typing
import time
from threading import Event, Thread
import threading
import datetime
#https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds


class RedditListener(commands.Cog, name="Reddit Listener"):
    """Listens for a new reddit post"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def redditlisten(self, context, subreddit, min_time):
        await context.send("Starting listen for the subreddit '" + subreddit + "' for " + min_time + " minutes")
        #await sendPosts(context, new_posts)

        reddit_data = getRedditData(subreddit)
        newest_post = reddit_data["data"]["children"][1]["data"]["name"]
        print(newest_post)


        t_end = time.time() + 60 * int(min_time)
        dt_started = datetime.datetime.utcnow()
        while time.time() < t_end:
            #dt_now = datetime.datetime.utcnow()
            #time_passed = (dt_now - dt_started).total_seconds()
            await blocking_func(5)
            newest_post = await runPostCheck(context, subreddit, newest_post)
            #if time_passed >= 5: #Run every 5 seconds
            #    newest_post = await runPostCheck(context, subreddit, newest_post)
            #    dt_started = dt_now

        await context.send("Completed listen")
        #await sendPosts(context, new_posts)

    #await context.reply("Your file is:", file=discord.File(file, "list_of_commits.txt"))

async def runPostCheck(context, subreddit, newest_post):
    reddit_data = getRedditData(subreddit)
    #print(reddit_data)
    new_post = reddit_data["data"]["children"][0]["data"]["name"]
    print("Checking new: " + new_post + " against newest: " + str(newest_post))
    if new_post == newest_post:
        return new_post
    
    print("is a new post")
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
    #response = urllib.request.urlopen(url).read()
    response = requests.get(url, headers = {'User-agent': 'your bot 0.1'}).text
    data = json.loads(response) #.decode('utf-8')
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
