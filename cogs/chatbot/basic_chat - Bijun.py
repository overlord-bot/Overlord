# Basic Chat Response
import random 
import io
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime
from datetime import date
import asyncio
        
                   
class ExtraFunc(commands.Cog, name="Additional Function "):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()  
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        if 'rick roll' in message.content.lower():
            await message.channel.send("https://c.tenor.com/_4YgA77ExHEAAAAd/rick-roll.gif")
            await message.channel.send("Never Gonna Give You Up!")
            await message.channel.send("Never Gonna Let You Down!")
        GREETING_INPUTS = ("hello", "greetings", "sup", "what's up","hey",)
        for word in message.content.split():
            if word.lower() in GREETING_INPUTS:
                await message.channel.send(random.choice(GREETING_INPUTS))
        
        if "!count" in message.content.lower():
            if  "sec" in message.content.lower():
                
                times = ""
                for i in range(0,len(message.content.lower())):
                    if message.content.lower()[i].isdigit() :
                        times+=message.content.lower()[i]
                times = int(times)
                times *= 10
                await message.channel.send("Start counting {} seconds!".format(int(times/10)))
                count = times
                while count:
                    if(count == (times/2)):
                        await message.channel.send("{} seconds left!".format(count/10))
                    await asyncio.sleep(0.1)
                    count -= 1
                await message.channel.send("TIME'S UP!")
                await message .channel.send("https://media1.giphy.com/media/xUOxfb3UW3H12DJ7m8/giphy.gif")
        
        if "!count" in message.content.lower():
            if  "min" in message.content.lower():
                times = ""
                for i in range(0,len(message.content.lower())):
                    if message.content.lower()[i].isdigit() :
                        times+=message.content.lower()[i]
                times = int(times)
                times *= 10
                await message.channel.send("Start counting {} minutes!".format(int(times/10)))
                count = times
                while count:

                    if(count == ((times/2))):
                        await message.channel.send("{} minutes left!".format(times/20))
                    await asyncio.sleep(6)
                    count -= 1
                await message.channel.send("TIME'S UP!")
                await message .channel.send("https://media1.giphy.com/media/xUOxfb3UW3H12DJ7m8/giphy.gif")
        
    '''
    @commands.command()
    async def count(self,message, arg1,arg2):
        if arg2 == "min":
            times = int(arg1)
            times*=10
            await message.channel.send("Start counting {} minutes!".format(int(times/10)))
            count = times
            while count!=0:
                if(count == (times/2)+5):
                    await message.channel.send("{} minutes left!".format(times/20))
                asyncio.sleep(6)
                count -= 1
            await message.channel.send("TIME'S UP!")
            await message.channel.send("https://media1.giphy.com/media/xUOxfb3UW3H12DJ7m8/giphy.gif")
        elif arg2 == "sec":
            times = int(arg1)
            times*=10
            await message.channel.send("Start counting {} seconds!".format(int(times/10)))
            count = times
            while count!=0:
                if(count == times/2):
                    await message.channel.channel.send("{} seconds left!".format(count/10))
                asyncio.sleep(1)
                count -= 1
            await message.channel.send("TIME'S UP!")
            await message.channel.send("https://media1.giphy.com/media/xUOxfb3UW3H12DJ7m8/giphy.gif")
    '''
    @commands.command()
    @commands.has_permissions(ban_members = True,administrator = True)
    async def ban(self,ctx,Member: discord.Member, reasons=None):
        await Member.ban(reason = reasons)
        'await ctx.guild.ban(Member,reason=reasons)'
        
    @commands.command()
    @commands.has_permissions(ban_members = True,administrator = True)
    async def unban(self,ctx,Member: discord.Member, reasons=None):
        await Member.unban(reason = reasons)
        
    @commands.command()
    @commands.has_permissions(ban_members = True,administrator = True)
    async def mute(self,ctx,Member: discord.Member, reasons=None):
        muterole = discord.utils.get(ctx.guild.roles,name="Muted")
        
        if not muterole:
            muterole = await ctx.guild.create_role(name = "Muted")
            for channel in ctx.guild.channels:
                await channel.set_permmissions(muterole, speak = False, send_message=False)  
        role_get = discord.utils.get(Member.guild.roles, name="Friends") #Returns a role object.
        await Member.remove_roles(role_get) #Remove the role (object) from the user.   
        await Member.add_roles(muterole,reason=reasons)
        await ctx.send(f"Muted {Member.mention} for reason {reasons}")  
    
    @commands.command()
    @commands.has_permissions(ban_members = True,administrator = True)
    async def unmute(self,ctx,Member: discord.Member, reasons=None):
        muterole = discord.utils.get(ctx.guild.roles,name="Muted")
        role_get = discord.utils.get(Member.guild.roles, name="Friends") #Returns a role object.
        await Member.remove_roles(muterole,reason=reasons) #Remove the role (object) from the user.   
        await Member.add_roles(role_get)
        await ctx.send(f"Unmuted {Member.mention} for reason {reasons}")
        
async def setup(bot):
    await bot.add_cog(ExtraFunc(bot))
