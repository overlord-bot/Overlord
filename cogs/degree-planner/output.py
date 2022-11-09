from discord.ext import commands
import discord
from enum import Enum
from collections import OrderedDict
from .user import *
import time


class OUT(Enum):
    DISCORD_CHANNEL = 1
    DISCORD_PRIVATE_MSG = 2
    CONSOLE = 3
    NONE = 100


class ATTRIBUTE(Enum):
    CHANNEL = 1
    USER = 2
    FLAG = 3
    FANCY = 10


class Output():

    """ Handles printing output to specified location
    
    Args:
        location (OUT): Enum that describes location to print into
        attributes (dict): {attribute name : attribute value}
            An attribute is additional information, some are required such
            as channel or user if we're printing to specific channels, 
            others are optional, such as fancy mode.
    """
    def __init__(self, location, attributes:dict=None):
        self.location = location
        self.channel = None
        self.flags = set()
        self.__msg_cache_hold = ""
        self.message_history = OrderedDict() # <message, time>

        self.last_message = None
        self.last_message_content = ''
        self.last_message_time = 1
        self.editlast = False

        if attributes != None and isinstance(attributes, dict):
            for k, v in attributes.items():
                if k == ATTRIBUTE.CHANNEL:
                    self.channel = v
                if k == ATTRIBUTE.USER:
                    self.channel = v.discord_user
                if k == ATTRIBUTE.FLAG:
                    self.flags.add(v)


    """ Print one line at a time to specified output

    Args:
        msg (string): message to print
    """
    async def print(self, msg):
        if self.location == OUT.CONSOLE:
            print(msg)
            return

        if self.location == OUT.DISCORD_CHANNEL or self.location == OUT.DISCORD_PRIVATE_MSG:
            if Flag.DEBUG in self.flags:
                print(msg)
                return
            if self.channel == None:
                print("no channel specified for printing message: " + msg)
                return
            if ATTRIBUTE.FANCY in self.flags:
                await self.print_fancy(msg)
                return
            await self.channel.send(msg)
            return


    """70 lines of pure organic undocumented spaghetti code for formatting and printing embeds written at 3am while sleep deprived, good luck
    """
    async def print_fancy(self, msg:str):
        if self.location == OUT.CONSOLE or self.channel == None:
            print("OUTPUT ERROR: can't print fancy")
            return

        # blocks represent a title/message

        # sanitize input:
        msg.replace('##', '')

        self.editlast = False
        # determines whether we should add on to the previous message or generate new one
        if len(msg) + len(self.last_message_content) < 1000 and time.time() - self.last_message_time < 3:
            self.editlast = True
            msg = self.last_message_content + "##" + msg

        # concatnate messages with same title or no titles
        msg_blocks = msg.split('##')
        title_element = ''
        message_element = ''
        msg_blocks_titled = []
        for e in msg_blocks:
            # if we do not find a title separator inside block
            if '/' not in e:
                # if this is the first message to be pushed, add title 'untitled'
                if not len(title_element):
                    title_element = 'untitled'
                message_element += '\n\n' + e
            else:
                # if there exists previous blocks to push
                if len(title_element):
                    msg_blocks_titled.append(title_element + "/" + message_element)
                title_element = e.split('/')[0]
                message_element = e.split('/')[1]
        msg_blocks_titled.append(title_element + "/" + message_element)

        # combines consecutive blocks with the same title
        msg_blocks_condensed = []
        title_element = ''
        message_element = ''
        for e in msg_blocks_titled:
            if e.split('/')[0] == title_element:
                message_element += '\n\n' + e.split('/')[1]
            else:
                if title_element != '':
                    msg_blocks_condensed.append(title_element + "/" + message_element)
                title_element = e.split('/')[0]
                message_element = e.split('/')[1]
        msg_blocks_condensed.append(title_element + "/" + message_element)

        # if duplicated titles are found, add a counter to the title so it's not duplicated
        titles = dict()
        for i in range(0, len(msg_blocks_condensed)):
            e = msg_blocks_condensed[i]
            element_title = e.split('/')[0]
            if element_title in titles:
                msg_blocks_condensed[i] = element_title + f" ({titles[element_title]})/" + e.split('/')[1]
                titles[element_title] += 1
            else:
                titles.update({element_title:1})

        # generate msg_blocks dictionary to be submitted to print_embed
        msg_blocks = OrderedDict()
        for e in msg_blocks_condensed:
            title_element = e.split("/")[0]
            message_element = e.split("/")[1]
            msg_blocks.update({title_element : message_element})
        
        await self.print_embed(msg_blocks)
        self.last_message_content = msg
        self.last_message_time = time.time()
        return


    async def print_embed(self, msg_blocks:dict):
        embed = discord.Embed(title="Degree Planner",color=discord.Color.blue())
        for k, v in msg_blocks.items():
            if len(k) == 0:
                embed.add_field(name=f"Untitled", value=v, inline = False)
            else:
                embed.add_field(name=k, value=v, inline = False)
        if self.editlast:
            await self.last_message.edit(embed=embed)
        else:
            self.last_message = await self.channel.send(embed=embed)
        return


    """ Creates a temporary cache to store strings, which can then be
        outputted at once when print_cache is called.

    Args:
        msg (string): message to hold
    """
    def print_hold(self, msg):
        self.__msg_cache_hold += msg + "\n"
        return


    """ Prints all content inside message cache, calls upon print() for printing
    """
    async def print_cache(self):
        if (len(self.__msg_cache_hold) > 1800 
                and (self.location == OUT.DISCORD_CHANNEL 
                or self.location == OUT.DISCORD_PRIVATE_MSG)):
            await self.print(f"message too long for discord, printing to console...")
            print(self.__msg_cache_hold)
        else:
            if self.location == OUT.CONSOLE:
                await self.print(f"{self.__msg_cache_hold}")
            else:
                fancy = False
                if ATTRIBUTE.FANCY in self.flags:
                    self.last_message_time = 1
                    self.flags.remove(ATTRIBUTE.FANCY)
                    fancy = True
                await self.print(f"```yaml\n{self.__msg_cache_hold}```")
                if fancy:
                    self.flags.add(ATTRIBUTE.FANCY)
        
        self.__msg_cache_hold = ""
        return
