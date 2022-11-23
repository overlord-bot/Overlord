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

class OUT(Enum):
    NONE = 0
    
    DISCORD_CHANNEL = 11

    CONSOLE = 21
    INFO = 22
    DEBUG = 23
    WARN = 24
    ERROR = 25

    CACHE = 30
    FILE = 31

class OUTTYPE(Enum):
    STRING = 1
    EMBED = 2
    JSON = 3

class Output():

    """ Handles printing output to specified location
    
    Args:
        output_location (OUT): Enum that describes location to print into
        output_type (OUTTYPE): How to format output
        discord_channel (channel): discord channel if printing to discord
        file (file): file to print to if printing to file
        combine_embeds (bool): whether to merge embeds when printing to discord
        signature (str): used for embed titles
    """
    def __init__(self, output_location:OUT, output_type:OUTTYPE=OUTTYPE.STRING, user=None, 
            discord_channel=None, file=None, combine_embeds:bool=True, signature:str=''):
        self.output_location = output_location
        self.output_type = output_type
        self.discord_channel = discord_channel
        self.file = file
        self.user = user

        self.__msg_cache_hold = ""
        self.json_cache = list()

        # for printing and editing discord embeds
        self.last_message_object = None
        self.last_message_content = ''
        self.last_message_time = 1
        self.edit_last_message = False

        self.message_max_length = 2000

        self.combine_message_time_limit = 5
        self.combine_embeds = combine_embeds

        if output_type == OUTTYPE.EMBED:
            self.message_max_length = 1000

        self.signature = signature

        logging.getLogger().setLevel(logging.DEBUG)


    """ Determines appropriate printing channel and prints message

    Args:
        msg (str): message to print
        
        logging_flag (OUT): temporary prints to this output location
            without altering the stored location within this object
    """
    async def print(self, msg:str, json_output:json=None, output_location:OUT=None, file_name:str=None) -> None:
        outlocation = self.output_location if output_location == None else output_location
     
        tagged_msg = f'{self.signature} {msg}'

        if outlocation == OUT.INFO:
            logging.info(tagged_msg)
        elif outlocation == OUT.DEBUG:
            logging.debug(tagged_msg)
        elif outlocation == OUT.WARN:
            logging.warning(tagged_msg)
        elif outlocation == OUT.ERROR:
            logging.error(tagged_msg)

        elif outlocation == OUT.CONSOLE:
            print(msg)

        # If printing to discord, will use block (title/message) formatting
        elif outlocation == OUT.DISCORD_CHANNEL:
            if self.discord_channel == None:
                logging.warning('OUTPUT ERROR: no output channel specified')
            elif self.output_type == OUTTYPE.EMBED:
                await self.print_embed(self.get_title_body_blocks(msg))
            else:
                await self.print_fancy(self.get_title_body_blocks(msg))

        elif (self.output_location == OUT.CACHE):
            self.json_cache.append(json_output)

        elif (self.output_location == OUT.FILE):
            f = open(file_name, 'a')
            f.write(msg)
            f.close


    """ Goes through each function to generate the blocks from original input string

    Args:
        msg (str): message to print

    Returns:
        msg_blocks (OrderedDict): ordered dictionary of (title/message) blocks where each
            member is guaranteed to be non-empty, and titles are all unique.
    """
    def get_title_body_blocks(self, msg):
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
        embed = discord.Embed(title=self.signature,color=user_color)
        for k, v in msg_blocks.items():
            embed.add_field(name='Untitled' if not len(k) else k.strip(), value=v, inline = False)
        if self.edit_last_message:
            await self.last_message_object.edit(embed=embed)
        else:
            self.last_message_object = await self.discord_channel.send(embed=embed)


    """ Prints blocks (title, body) as text
    """
    async def print_fancy(self, msg_blocks:OrderedDict):
        msg = ''
        for k, v in msg_blocks.items():
            msg += f"\u2800\n**{k}**: \n{v}\n"
        if self.edit_last_message:
            await self.last_message_object.edit(content=msg)
        else:
            self.last_message_object = await self.discord_channel.send(msg)


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
        if self.output_location == OUT.CONSOLE:
            await self.print(self.__msg_cache_hold, output_location=output_redirect)
        else:
            await self.print(f"```yaml\n{'None' if not len(self.__msg_cache_hold) else self.__msg_cache_hold}```", output_location=output_redirect)
        self.__msg_cache_hold = ""
        return


""" removes all non-alphanumeric characters from string

Args:
    msg (str): string to strip

Returns:
    msg (str): stripped string
"""
def cleanse(msg:str) -> str:
    re.sub(r'\W+', '', msg)
    return msg