from discord.ext import commands
import discord
import logging
from enum import Enum
from collections import OrderedDict
import time
import re
import json

DELIMITER_TITLE = '---'
DELIMITER_BLOCK = '###'
TAG_NOMERGE = '@nomerge'

DEGREE_PLANNER_SIGNATURE = '~~~ Great Sage ~~~'


class OUT(Enum):
    DISCORD_CHANNEL = 11
    DISCORD_PRIVATE_MSG = 12
    NONE = 0

    CONSOLE = 21
    INFO = 22 # INFORMATIONAL
    DEBUG = 23 # DETAILED STATUS NORMALLY HIDDEN
    WARN = 24 # SKILL ISSUE
    ERROR = 25 # PROGRAM ISSUE

    WEB = 100


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

        logging.getLogger().setLevel(logging.DEBUG)


    """ Determines appropriate printing channel and prints message

    Args:
        msg (str or dict): message to print
        logging_flag (OUT): temporary prints to this output location
            without altering the stored location within this object
    """
    async def print(self, msg:str, json_output:json=None, output_location=None) -> None:
        outloc = self.output_location
        if output_location != None and isinstance(output_location, OUT) and output_location.value//10 == 2:
            self.output_location = output_location
        
        tagged_msg = f'{DEGREE_PLANNER_SIGNATURE} {msg}'

        if self.output_location == OUT.INFO:
            logging.info(tagged_msg)
        elif self.output_location == OUT.DEBUG:
            logging.debug(tagged_msg)
        elif self.output_location == OUT.WARN:
            logging.warning(tagged_msg)
        elif self.output_location == OUT.ERROR:
            logging.error(tagged_msg)

        elif self.output_location == OUT.CONSOLE:
            print(msg)

        # If printing to discord, will use block (title/message) formatting
        elif (self.output_location == OUT.DISCORD_CHANNEL 
                or self.output_location == OUT.DISCORD_PRIVATE_MSG):
            if self.output_channel == None:
                logging.warning('OUTPUT ERROR: no output channel specified')
            elif ATTRIBUTE.EMBED in self.flags:
                await self.print_embed(self.get_blocks(msg))
            else:
                await self.print_fancy(self.get_blocks(msg))

        elif (self.output_location == OUT.WEB):
            self.on_output(json_output)

        self.output_location = outloc


    """ Goes through each function to generate the blocks from original input string

    Args:
        msg (str): message to print

    Returns:
        msg_blocks (OrderedDict): ordered dictionary of (title/message) blocks where each
            member is guaranteed to be non-empty, and titles are all unique.
    """
    def get_blocks(self, msg):
        msg = self.trim_to_limit(msg)
        msg = self.try_combine_previous(msg)
        blocks = self.format_title_and_body(msg)
        return blocks


    """ Trims message to abide by message limit, and adds appropriate delimiters such as yaml quotes

    Args:
        msg (str): message to print

    Returns:
        msg (str): trimmed message
    """
    def trim_to_limit(self, msg:str) -> str:
        if self.message_max_length < 101:
            return ''
        if len(msg) > self.message_max_length - 100:
            if msg[-3:] == '```':
                msg = msg[:self.message_max_length - 100] + '...\n```'
            else:
                msg = msg[:self.message_max_length - 100] + "..."
        return msg


    """ Determines whether to combine current message with previous one,
    and if so, combines the two strings.

    Args:
        msg (str): current message to print

    Returns:
        msg (str): merged string if merging does not violate any message length
            rules or 'no merge' tags, else returns original string minus tags.
    """
    def try_combine_previous(self, msg):
        self.edit_last_message = False
        # determines whether we should add on to the previous message or generate new one
        if (len(msg) + len(self.last_message_content) < self.message_max_length 
                and time.time() - self.last_message_time < self.combine_message_time_limit
                and not msg.startswith(TAG_NOMERGE)):
            self.edit_last_message = True
            msg = self.last_message_content + DELIMITER_BLOCK + msg
        msg = msg.replace(TAG_NOMERGE, '')
        return msg


    """ Formats string into a list of (title/message) blocks in the form of an OrderedDict

    Args:
        msg (str): message containing any number/combination of title and block delimiters

    Returns:
        msg_blocks (OrderedDict): ordered dictionary of (title/message) blocks where each
            member is guaranteed to be non-empty, and titles are all unique.
    """
    def format_title_and_body(self, msg:str) -> dict:
        # assigns a title to messages without titles
        msg_blocks = msg.split(DELIMITER_BLOCK)
        title_element = ''
        message_element = ''
        msg_blocks_titled = []
        for e in msg_blocks:
            # if we do not find a title separator inside block, merge with previous
            if DELIMITER_TITLE not in e:
                # if this is the first message to be pushed, add title 'untitled'
                if not len(title_element): 
                    title_element = 'Untitled'
                message_element += ('\n' if e.startswith('```') else '\n\u2022 ') + e
            else:
                # push previous blocks (title_element+DELIMITER+message_element) to list if any
                if len(title_element):
                    msg_blocks_titled.append(title_element + DELIMITER_TITLE + message_element)
                # assigns title and body to temporary variables
                title_element = e.split(DELIMITER_TITLE)[0]
                message_element = ('\n' if e.startswith('```') else '\u2022 ') + e.split(DELIMITER_TITLE)[1]
        msg_blocks_titled.append(title_element + DELIMITER_TITLE + message_element)

        # combines consecutive blocks with the same title
        msg_blocks_condensed = []
        title_element = ''
        message_element = ''
        for e in msg_blocks_titled:
            # if we find the title of this element to match the previous, merge bodies together
            if e.split(DELIMITER_TITLE)[0] == title_element:
                message_element += '\n' + e.split(DELIMITER_TITLE)[1]
            else:
                # push previous blocks (title_element+DELIMITER+message_element) to list if any
                if len(title_element):
                    msg_blocks_condensed.append(title_element + DELIMITER_TITLE + message_element)
                 # assigns title and body to temporary variables
                title_element = e.split(DELIMITER_TITLE)[0]
                message_element = e.split(DELIMITER_TITLE)[1]
        msg_blocks_condensed.append(title_element + DELIMITER_TITLE + message_element)

        # if duplicated titles are found, add a counter to the title so it's not duplicated
        titles = dict()
        for i in range(0, len(msg_blocks_condensed)):
            e = msg_blocks_condensed[i]
            element_title = e.split(DELIMITER_TITLE)[0]
            if element_title in titles:
                msg_blocks_condensed[i] = element_title + f" ({titles[element_title]}){DELIMITER_TITLE}" + e.split(DELIMITER_TITLE)[1]
                titles[element_title] += 1
            else:
                titles.update({element_title:1})

        # generate msg_blocks dictionary to be submitted to print_embed
        msg_blocks = OrderedDict()
        for e in msg_blocks_condensed:
            title_element = e.split(DELIMITER_TITLE)[0]
            message_element = e.split(DELIMITER_TITLE)[1]
            msg_blocks.update({title_element : message_element})

        self.last_message_content = msg
        self.last_message_time = time.time()
        return msg_blocks


    """ Prints blocks (titles, body) as embed
    """
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


    """ Prints blocks (title, body) as text
    """
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
        msg = msg.replace(DELIMITER_BLOCK, ': ')
        msg = msg.replace(DELIMITER_TITLE, ': ')
        msg = msg.replace(TAG_NOMERGE, '')
        self.__msg_cache_hold += msg + "\n"
        return


    """ Prints all content inside message cache, calls upon print() for printing
    """
    async def print_cache(self, output_redirect=None):
        if (len(self.__msg_cache_hold) > 1800 
                and (self.output_location == OUT.DISCORD_CHANNEL 
                or self.output_location == OUT.DISCORD_PRIVATE_MSG)):
            await self.print(f"message too long for discord, printing to console...")
            print(self.__msg_cache_hold)
        else:
            if self.output_location == OUT.CONSOLE:
                await self.print(f"{self.__msg_cache_hold}", output_location=output_redirect)
            else:
                await self.print(f"```yaml\n{'None' if not len(self.__msg_cache_hold) else self.__msg_cache_hold}```", output_location=output_redirect)
        self.__msg_cache_hold = ""
        return

    def on_output(self, json_message:json):
        raise NotImplementedError


""" removes all non-alphanumeric characters from string

Args:
    msg (str): string to strip

Returns:
    msg (str): stripped string
"""
def cleanse(msg:str) -> str:
    re.sub(r'\W+', '', msg)
    return msg