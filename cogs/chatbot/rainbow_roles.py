from array import *
from discord.ext import commands
import discord

from ..utils.output import *

VERSION = "dev 1.1"

OUTERROR = Output(OUT.ERROR)
OUTWARNING = Output(OUT.WARN)
OUTINFO = Output(OUT.INFO)
OUTDEBUG = Output(OUT.DEBUG)
OUTCONSOLE = Output(OUT.CONSOLE)

RED = 0xf5cdd6
ORANGE = 0xf5e1cd
YELLOW = 0xf5f1cd
GREEN = 0xd6f5cd
TEAL = 0xcdf5f1
BLUE = 0xcdd4f5
VIOLET = 0xe8cdf5
MAGENTA = 0xe6a6d3

MAX_COLORS = 8

class rainbow_roles(commands.Cog, name="Rainbow Roles"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if (message.content == 'rainbowfy'):
            await self.rainbowfy(message.guild, Output(OUT.DISCORD_CHANNEL, OUTTYPE.EMBED, discord_channel=message.channel, signature='Rainbow Roles'))
        if (message.content == 'cleanse'):
            await self.cleanse(message.guild, Output(OUT.DISCORD_CHANNEL, OUTTYPE.EMBED, discord_channel=message.channel, signature='Rainbow Roles'))
        if (message.content == 'deep cleanse' or 'tidy up the fucking roles' in message.content):
            await self.deep_cleanse(message.guild, Output(OUT.DISCORD_CHANNEL, OUTTYPE.EMBED, discord_channel=message.channel, signature='Rainbow Roles'))


    async def cleanse(self, guild, output=None):
        if output == None:
            output = Output(OUT.CONSOLE)
        for m in guild.members:
            for i in range(1, MAX_COLORS+1):
                await m.remove_roles(discord.utils.get(guild.roles, name=str(i)))
        await output.print(f'Cleanse{DELIMITER_TITLE}cleansed the roles!')


    async def deep_cleanse(self, guild, output=None):
        if output == None:
            output = Output(OUT.CONSOLE)
        for i in range(1, MAX_COLORS+1):
            if discord.utils.get(guild.roles, name = str(i)): await discord.utils.get(guild.roles, name=str(i)).delete()
        await output.print(f'Deep Cleaning{DELIMITER_TITLE}roles reduced to atoms')


    async def rainbowfy(self, guild, output=None):
        if output == None:
            output = Output(OUT.CONSOLE)
        if not discord.utils.get(guild.roles, name = '1'): await guild.create_role(name='1', color=discord.Colour(RED))
        if not discord.utils.get(guild.roles, name = '2'): await guild.create_role(name='2', color=discord.Colour(ORANGE))
        if not discord.utils.get(guild.roles, name = '3'): await guild.create_role(name='3', color=discord.Colour(YELLOW))
        if not discord.utils.get(guild.roles, name = '4'): await guild.create_role(name='4', color=discord.Colour(GREEN))
        if not discord.utils.get(guild.roles, name = '5'): await guild.create_role(name='5', color=discord.Colour(TEAL))
        if not discord.utils.get(guild.roles, name = '6'): await guild.create_role(name='6', color=discord.Colour(BLUE))
        if not discord.utils.get(guild.roles, name = '7'): await guild.create_role(name='7', color=discord.Colour(VIOLET))
        if not discord.utils.get(guild.roles, name = '8'): await guild.create_role(name='8', color=discord.Colour(MAGENTA))

        await output.print(f'Rainbowfy{DELIMITER_TITLE}created roles')

        # make an ordered dictionary of <top role:members>
        # so that we can assign the colors in the appropriate order
        top_roles = OrderedDict()
        for m in guild.members:
            toprole = top_role(guild, m)
            if top_roles.get(toprole) == None:
                top_roles.update({toprole:[m]})
            else:
                top_roles[toprole].append(m)

        top_roles = dict(sorted(top_roles.items(), reverse=True))

        # convert the dictionary into a list while sorting all members
        # within each dictionary entry
        members = list()
        for ms in top_roles.values():
            members.extend(sort_members(ms))
        
        i = 0
        for m in members:
            await m.add_roles(discord.utils.get(guild.roles, name=str( int( 1+i*MAX_COLORS/(len(members)) ) )))
            i += 1

        await output.print('server successfully rainbowfied!')


"""
HELPER FUNCTIONS
"""

def top_role(guild, member):
    role = discord.utils.get(guild.roles, name='@everyone')
    for r in member.roles:
        if r.hoist:
            role = r
    return role

def sort_members(members):
    members_dict = OrderedDict()
    for m in members:
        if m.nick == None: 
            members_dict.update({m.name:m})
        else: 
            members_dict.update({m.nick:m})
    return dict(sorted(members_dict.items())).values()


async def setup(bot):
    await bot.add_cog(rainbow_roles(bot))
