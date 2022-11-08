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
        #self.user = None
        self.channel = None
        self.flags = set()
        self.__msg_cache_hold = ""
        self.message_history = OrderedDict() # <message, time>

        self.last_message = None
        self.last_message_content = ''
        self.last_message_time = 1

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
    async def print_fancy(self, msg):
        if self.location == OUT.CONSOLE or self.channel == None:
            print("OUTPUT ERROR: can't print fancy")
            return
        edit_last = False
        if len(msg) + len(self.last_message_content) < 1000 and time.time() - self.last_message_time < 3:
            edit_last = True
        if edit_last:
            msg = self.last_message_content + "##" + msg
        # concatnate messages with same title or no titles
        msg_split = msg.split('##')
        title = ''
        last_valid_msg = ''
        msg_split_valid = []
        for e in msg_split:
            if '/' not in e:
                last_valid_msg += '\n\n' + e
            else:
                if title != '':
                    msg_split_valid.append(title + "/" + last_valid_msg)
                title = e.split('/')[0]
                last_valid_msg = e.split('/')[1]
        msg_split_valid.append(title + "/" + last_valid_msg)

        msg_split_valid2 = []
        last_title = ''
        last_msg = ''
        for e in msg_split_valid:
            if e.split('/')[0] == last_title:
                last_msg += '\n\n' + e.split('/')[1]
            else:
                if last_title != '':
                    msg_split_valid2.append(last_title + "/" + last_msg)
                last_title = e.split('/')[0]
                last_msg = e.split('/')[1]
        msg_split_valid2.append(last_title + "/" + last_msg)


        msg_combo = OrderedDict()
        #print("original msg: " + msg)
        #print("valid split: " + str(msg_split_valid))
        #print("valid split2: " + str(msg_split_valid2))
        titledict = dict()
        for i in range(0, len(msg_split_valid2)):
            e = msg_split_valid2[i]
            elementtitle = e.split('/')[0]
            if elementtitle in titledict:
                msg_split_valid2[i] = elementtitle + f" ({titledict[elementtitle]})/" + e.split('/')[1]
                titledict[elementtitle] = titledict[elementtitle] + 1
            else:
                titledict.update({elementtitle:1})
        i = 1
        for e in msg_split_valid2:
            msg_splitsplit = e.split("/")
            msg_combo.update({msg_splitsplit[0] if len(msg_splitsplit) > 1 else f'{i}. Output' : msg_splitsplit[1] if len(msg_splitsplit) > 1 else msg_splitsplit[0]})
            i += 1
        embed = discord.Embed(title="Degree Planner",color=discord.Color.blue())
        for k, v in msg_combo.items():
            if len(k) == 0:
                embed.add_field(name=f"Untitled", value=v, inline = False)
            else:
                embed.add_field(name=k, value=v, inline = False)
        if edit_last:
            await self.last_message.edit(embed=embed)
        else:
            self.last_message = await self.channel.send(embed=embed)
        self.last_message_content = msg
        self.last_message_time = time.time()
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
