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
    EMBED = 10
    FANCY = 11


class Output():

    """ Handles printing output to specified location
    
    Args:
        output_location (OUT): Enum that describes location to print into
        attributes (dict): {attribute name : attribute value}
            An attribute is additional information, some are required such
            as channel or user if we're printing to specific channels, 
            others are optional, such as fancy mode.
    """
    def __init__(self, output_location, attributes:dict=None):
        self.output_location = output_location
        self.output_channel = None
        self.user = None
        self.flags = set()

        self.__msg_cache_hold = ""

        self.last_message_object = None
        self.last_message_content = ''
        self.last_message_time = 1
        self.edit_last_message = False

        self.message_max_length = 2000
        self.combine_message_time_limit = 5
        self.body_delimiter = '---'
        self.block_delimiter = '###'
        self.no_merge = '@nomerge'

        if attributes != None and isinstance(attributes, dict):
            for k, v in attributes.items():
                if k == ATTRIBUTE.CHANNEL:
                    self.output_channel = v
                if k == ATTRIBUTE.USER:
                    self.output_channel = v.discord_user
                    self.user = v
                if k == ATTRIBUTE.FLAG:
                    self.flags.add(v)

        if ATTRIBUTE.EMBED in self.flags:
            self.message_max_length = 1000


    """ Print one line at a time to specified output

    Args:
        msg (str): message to print
    """
    async def print(self, msg):
        if self.output_location == OUT.CONSOLE or Flag.DEBUG in self.flags:
            print(msg)

        elif self.output_location == OUT.DISCORD_CHANNEL or self.output_location == OUT.DISCORD_PRIVATE_MSG:
            if self.output_channel == None:
                print("OUTPUT ERROR: no channel specified for printing message: " + msg)
            elif ATTRIBUTE.EMBED in self.flags:
                await self.print_embed(self.get_blocks_with_updates(msg))
            else:
                await self.print_fancy(self.get_blocks_with_updates(msg))


    def trim_to_limit(self, msg):
        if len(msg) > self.message_max_length - 100:
            if msg[-3:] == '```':
                msg = msg[:self.message_max_length - 100] + '...\n```'
            else:
                msg = msg[:self.message_max_length - 100] + "..."
        return msg


    def combine_previous(self, msg):
        self.edit_last_message = False
        # determines whether we should add on to the previous message or generate new one
        if (len(msg) + len(self.last_message_content) < self.message_max_length 
                and time.time() - self.last_message_time < self.combine_message_time_limit
                and not msg.startswith(self.no_merge)):
            self.edit_last_message = True
            msg = self.last_message_content + self.block_delimiter + msg
        msg = msg.replace('@nomerge', '')
        return msg


    """Takes in a string with ### to delimit blocks and self.delimiter to delimit title from body

    returns a dictionary with each entry being a title:body block
    """
    def format_title_and_body(self, msg:str) -> dict:
        # concatnate messages with same title or no titles
        msg_blocks = msg.split(self.block_delimiter)
        title_element = ''
        message_element = ''
        msg_blocks_titled = []
        for e in msg_blocks:
            # if we do not find a title separator inside block, merge with previous
            if self.body_delimiter not in e:
                # if this is the first message to be pushed, add title 'untitled'
                if not len(title_element): 
                    title_element = 'Untitled'
                message_element += ('\n' if e.startswith('```') else '\n\u2022 ') + e
            else:
                # push previous blocks to list if any
                if len(title_element):
                    msg_blocks_titled.append(title_element + self.body_delimiter + message_element)
                # assigns title and body to temporary variables
                title_element = e.split(self.body_delimiter)[0]
                message_element = ('\n' if e.startswith('```') else '\u2022 ') + e.split(self.body_delimiter)[1]
        msg_blocks_titled.append(title_element + self.body_delimiter + message_element)

        # combines consecutive blocks with the same title
        msg_blocks_condensed = []
        title_element = ''
        message_element = ''
        for e in msg_blocks_titled:
            if e.split(self.body_delimiter)[0] == title_element:
                message_element += '\n' + e.split(self.body_delimiter)[1]
            else:
                if title_element != '':
                    msg_blocks_condensed.append(title_element + self.body_delimiter + message_element)
                title_element = e.split(self.body_delimiter)[0]
                message_element = e.split(self.body_delimiter)[1]
        msg_blocks_condensed.append(title_element + self.body_delimiter + message_element)

        # if duplicated titles are found, add a counter to the title so it's not duplicated
        titles = dict()
        for i in range(0, len(msg_blocks_condensed)):
            e = msg_blocks_condensed[i]
            element_title = e.split(self.body_delimiter)[0]
            if element_title in titles:
                msg_blocks_condensed[i] = element_title + f" ({titles[element_title]}){self.body_delimiter}" + e.split(self.body_delimiter)[1]
                titles[element_title] += 1
            else:
                titles.update({element_title:1})

        # generate msg_blocks dictionary to be submitted to print_embed
        msg_blocks = OrderedDict()
        for e in msg_blocks_condensed:
            title_element = e.split(self.body_delimiter)[0]
            message_element = e.split(self.body_delimiter)[1]
            msg_blocks.update({title_element : message_element})

        self.last_message_content = msg
        self.last_message_time = time.time()
        return msg_blocks


    def get_blocks_with_updates(self, msg):
        msg = self.trim_to_limit(msg)
        msg = self.combine_previous(msg)
        blocks = self.format_title_and_body(msg)
        return blocks


    async def print_embed(self, msg_blocks:OrderedDict):
        user_color = discord.Color.from_rgb(172,64,184)
        if self.user != None:
            user_color = self.user.discord_user.color
        embed = discord.Embed(title='Degree Planner',color=user_color)
        for k, v in msg_blocks.items():
            embed.add_field(name='Untitled' if not len(k) else k.strip(), value=v, inline = False)
        if self.edit_last_message:
            await self.last_message_object.edit(embed=embed)
        else:
            self.last_message_object = await self.output_channel.send(embed=embed)


    async def print_fancy(self, msg_blocks:OrderedDict):
        msg = ''
        for k, v in msg_blocks.items():
            msg += f"\u2800\n**{k}**: \n{v}\n"
        if self.edit_last_message:
            await self.last_message_object.edit(content=msg)
        else:
            self.last_message_object = await self.output_channel.send(msg)


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
    async def print_cache(self, embeds=True):
        if (len(self.__msg_cache_hold) > 1800 
                and (self.output_location == OUT.DISCORD_CHANNEL 
                or self.output_location == OUT.DISCORD_PRIVATE_MSG)):
            await self.print(f"message too long for discord, printing to console...")
            print(self.__msg_cache_hold)
        else:
            if self.output_location == OUT.CONSOLE:
                await self.print(f"{self.__msg_cache_hold}")
            else:
                fancy = False
                if ATTRIBUTE.EMBED in self.flags and not embeds:
                    self.last_message_time = 1
                    self.flags.remove(ATTRIBUTE.EMBED)
                    fancy = True
                await self.print(f"```yaml\n{'None' if not len(self.__msg_cache_hold) else self.__msg_cache_hold}```")
                if fancy:
                    self.flags.add(ATTRIBUTE.EMBED)
        self.__msg_cache_hold = ""
        return
