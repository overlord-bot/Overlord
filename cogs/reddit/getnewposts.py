from hashlib import new
import urllib.request #python3 bot.py -fast -load reddit
import requests
#from urllib.request import Request, urlopen
import json

import discord
from discord.ext import commands



class NewRedditPosts(commands.Cog, name="Newest Reddit Post Retriever"):
    """Get new reddit posts"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newpost(self, context, subreddit, amount):
        print(amount)
        if amount.isdigit():
            amount = int(amount)
        else:
            await context.reply("Input possible integer")
            return

        if amount < 1 or amount > 24:
            await context.reply("Invalid amount input. Must be between 1 and 24")
            return
        
        reddit_data = getRedditData(subreddit)
        if reddit_data["data"]["dist"] == 0:
            await context.reply("Invalid subreddit / Error fetching subreddits")
            return
        newest_post = reddit_data["data"]["children"][int(amount)]["data"]["name"]

        new_posts = getNewPosts(context, reddit_data, newest_post)

        
        await sendPosts(context, new_posts, subreddit, amount)

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


async def sendPosts(context, new_posts, subreddit, amount):
    embedMessage = getEmbedMessage(new_posts, subreddit, amount)
    await context.send(embed=embedMessage)
    #for num_post in range(len(new_posts)):
    #    post = new_posts[num_post]
    #    embedMessage = getEmbedMessage(post)
    #    await context.send(embed=embedMessage)

def getEmbedMessage(posts, subreddit, amount):
    embed = discord.Embed(title="Displaying the {} newest posts from {}".format(amount, subreddit))
    for num_post in range(len(posts)):
        post = posts[num_post]
        embed.add_field(name=post["title"], value="https://www.reddit.com" + post["permalink"], inline=False)
    return embed    
        
    
async def setup(bot):
    await bot.add_cog(NewRedditPosts(bot))
