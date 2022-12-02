from array import *
from discord.ext import commands
import discord
from random import SystemRandom as sr
import time

from ..utils.output import *

class rainbow_roles(commands.Cog, name="Rainbow Roles"):

    def __init__(self, bot):
        self.bot = bot
        self.lock = False
        self.version = '1.1'
        self.colors = list()

    """ Creates a list of the colors needed for the roles
    """
    def set_rainbow(self):
        self.colors.clear()
        self.colors.append(0xf5cdd6) # red
        self.colors.append(0xf5e1cd) # orange
        self.colors.append(0xf5f1cd) # yellow
        self.colors.append(0xd6f5cd) # green
        self.colors.append(0xcdf5f1) # teal
        self.colors.append(0xcdd4f5) # blue
        self.colors.append(0xe8cdf5) # violet
        self.colors.append(0xe6a6d3) # magenta

    """ Creates a list of the colors needed for the roles
    """
    def set_rainbow2(self):
        self.colors.clear()
        self.colors.append(0xf5cdd6) # red
        self.colors.append(0xf5e1cd) # orange
        self.colors.append(0xf5f1cd) # yellow
        self.colors.append(0xd6f5cd) # green
        self.colors.append(0xcdf5f1) # teal
        self.colors.append(0xcdd4f5) # blue
        self.colors.append(0xe8cdf5) # violet
        self.colors.append(0xe6a6d3) # magenta

    """ Creates a list of the colors needed for the roles
    """
    def set_random(self):
        self.colors.clear()
        gen = sr()
        for i in range(0,20):
            self.colors.append(gen.randrange(255**3-1))

    
    @commands.command()
    async def rainbowfy(self, ctx, args=None):
        output = Output(OUT.DISCORD_CHANNEL, OUTTYPE.EMBED, discord_channel=ctx.channel, signature='Rainbow Roles')
        if args == None:
            if self.lock:
                await output.print(f'ERROR{DELIMITER_TITLE}Please hold while operation is in progress')
                return
            self.lock = True
            self.set_rainbow()
            await self.roles_paint(ctx.guild, output)
            self.lock = False
        elif args == 'random':
            if self.lock:
                await output.print(f'ERROR{DELIMITER_TITLE}Please hold while operation is in progress')
                return
            self.lock = True
            self.set_random()
            await self.roles_paint(ctx.guild, output)
            self.lock = False
    
    @commands.command()
    async def cleanse(self, ctx, args=None):
        output = Output(OUT.DISCORD_CHANNEL, OUTTYPE.EMBED, discord_channel=ctx.channel, signature='Rainbow Roles')
        if args == None:
            if self.lock:
                await output.print(f'ERROR{DELIMITER_TITLE}Please hold while operation is in progress')
                return
            self.lock = True
            await self.roles_cleanse(ctx.guild, output)
            self.lock = False
        elif args == 'deep':
            if self.lock:
                await output.print(f'ERROR{DELIMITER_TITLE}Please hold while operation is in progress')
                return
            self.lock = True
            await self.roles_deep_cleanse(ctx.guild, output)
            self.lock = False
    
    @commands.command()
    async def rainbow(self, ctx):
        output = Output(OUT.DISCORD_CHANNEL, OUTTYPE.EMBED, discord_channel=ctx.channel, signature='Rainbow Roles')
        await output.print(f'Info{DELIMITER_TITLE}Rainbow Roles version: {self.version}')
        await output.print(f'Info{DELIMITER_TITLE}Commands: !rainbowfy, !cleanse, !deep cleanse, !rainbow roles/!rainbow version')

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot.user or message.author.bot:
            return

        if ('tidy up the fucking roles please' in message.content):
            output = Output(OUT.DISCORD_CHANNEL, OUTTYPE.EMBED, discord_channel=message.channel, signature='Rainbow Roles')
            self.lock = True
            await self.roles_deep_cleanse(message.guild, output)
            self.lock = False
            

    """ Deassigns color roles from everyone, but doesn't delete the roles themselves
    """
    async def roles_cleanse(self, guild, output=None):
        if output == None:
            output = Output(OUT.CONSOLE)
        
        for m in guild.members:
            for i in range(0, 20):
                if discord.utils.get(guild.roles, name = str(i)): await m.remove_roles(discord.utils.get(guild.roles, name=str(i)))
        await output.print(f'Cleanse{DELIMITER_TITLE}cleansed the roles!')


    """ Deletes all color roles
    """
    async def roles_deep_cleanse(self, guild, output=None):
        if output == None:
            output = Output(OUT.CONSOLE)

        for i in range(0, 20):
            if discord.utils.get(guild.roles, name = str(i)): await discord.utils.get(guild.roles, name=str(i)).delete()
        await output.print(f'Deep Cleaning{DELIMITER_TITLE}roles reduced to atoms')


    """ Creates the color roles (labelled by a number starting from 0), and assigns everyone to it in an even distribution
        among all the colors
    """
    async def roles_paint(self, guild, output=None):
        if output == None:
            output = Output(OUT.CONSOLE)

        for i in range(0, len(self.colors)):
            if discord.utils.get(guild.roles, name = str(i)): await discord.utils.get(guild.roles, name=str(i)).delete()
            await guild.create_role(name=str(i), color=discord.Colour(self.colors[i]))

        # make an ordered dictionary of <top role:members>
        # so that we can assign the colors in the appropriate order
        top_roles = OrderedDict()
        for m in guild.members:
            toprole = top_role(guild, m)
            #print('top role of : ' + str(m) + ' ' + str(toprole))
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
            await m.add_roles(discord.utils.get(guild.roles, name=str( int((i/((len(members) - 1) if len(members) > 1 else 1)) * len(self.colors) * 0.99))))
            i += 1

        await output.print(f'Rainbowfy{DELIMITER_TITLE}Server successfully rainbowfied!')


"""
HELPER FUNCTIONS
"""

"""
Args:
    guild (guild): discord server
    member (member): discord member object

Returns:
    role (role): discord role that is the highest ranking hoisted role of the given member
        hoisted role means it's a role displayed separately on the sidebar.
"""
def top_role(guild, member):
    role = discord.utils.get(guild.roles, name='@everyone')
    for r in member.roles:
        if r.hoist:
            role = r
    return role

""" If you're asking 'eggy why didn't you just feed a custom sort function to the provided sort()
     instead of generating all this bullshit' well you'll be absolutely correct 👍

Args:
    members (list): list of members to sort alphabetically by nickname (name if nick not available)

Returns:
    members (list): it's the members list but sorted
"""
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
