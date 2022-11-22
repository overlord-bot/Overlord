# Basic Chat Response
import random 
import io
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime
from datetime import date
import asyncio
import json 
import jsonpickle
       
class ExtraFunc(commands.Cog, name="Additional Function "):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()  
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        
       
        
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
            perms = discord.Permissions(speak = False, send_messages=False,read_messages=True)
            muterole = await ctx.guild.create_role(name = "Muted",permissions=perms)
            #for channel in ctx.guild.channels:
                #await channel.set_permmissions(muterole, speak = False, send_message=False,read_messages=True)  
        group = {}
        with open("./cogs/chatbot/Roles.json","r") as f:
            js=f.read()
        if len(js) == 0:
            var = json.dumps(group)
            f = open("./cogs/chatbot/Roles.json", "w")
            f.write(var)
            f.close()
        else:
            group = json.loads(js) #Group dictionary
        data = {} #Detail data for each member
        
        
        Roles = []
        for role in Member.roles:
            if(role.name!="@everyone"):
                Roles.append(role.id)
        
        data["was"] = Roles
        data["now"] = muterole.id
        data["Time"] = reasons
        group[str(Member.id)] = data
        print(group)
        var = json.dumps(group)
        f = open("./cogs/chatbot/Roles.json", "w")
        f.write(var)
        f.close()
        'await Member.remove_roles(Member.roles) #Remove the role (object) from the user.  '
        await Member.edit(roles=[muterole])
        'await Member.add_roles(muterole,reason=reasons)'
        await ctx.send(f"Muted {Member.mention} for reason {reasons}")  
    
    @commands.command()
    @commands.has_permissions(ban_members = True,administrator = True)
    async def unmute(self,ctx,Member: discord.Member, reasons=None):
        muterole = discord.utils.get(ctx.guild.roles,name="Muted")
        
        group = {}
        with open("./cogs/chatbot/Roles.json","r") as f:
            js=f.read()
        if len(js) == 0:
            var = json.dumps(group)
            f = open("./cogs/chatbot/Roles.json", "w")
            f.write(var)
            f.close()
        else:
            group = json.loads(js) #Group dictionary
        data = {}
        Roles = []
        for role in ctx.guild.roles:
            print(type(role.id))
        for role in group[str(Member.id)]["was"]:
            
            role_get = discord.utils.get(ctx.guild.roles, id=int(role)) #Returns a role object.
            print(role_get.id)
            await Member.add_roles(role_get)
            print(role_get.id)
            Roles.append(role);
            
        data["was"] = muterole.id
        data["now"] = Roles
        data["Time"] = reasons
        group[str(Member.id)] = data
        print(group)
        var = json.dumps(group)
        f = open("./cogs/chatbot/Roles.json", "w")
        f.write(var)
        f.close()
        await Member.remove_roles(muterole,reason=reasons) #Remove the role (object) from the user.   
        
        await ctx.send(f"Unmuted {Member.mention} for reason {reasons}")
    
        
async def setup(bot):
    await bot.add_cog(ExtraFunc(bot))
