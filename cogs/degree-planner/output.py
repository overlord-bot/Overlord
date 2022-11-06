from enum import Enum
from .user import Flag

class OUT(Enum):
    DISCORD_CHANNEL = 1
    DISCORD_PRIVATE_MSG = 2
    CONSOLE = 3

class ATTRIBUTE(Enum):
    CHANNEL = 1
    USER = 2
    FLAG = 3

# abstracts outputting data without needing to specify things like message, user, etc
class Output():

    #--------------------------------------------------------------------------
    # HOW TO USE THIS CLASS:
    #
    # specify a location to print out to, must be of type OUT (OUT is an enum)
    #
    # specify any attributes. For example, if we want to print to the user's
    # DM, then we must specify a user object. Attributes must be of type
    # ATTRIBUTE (enum)
    #
    # all attributes should be given in the form of a dictionary, where
    # { attribute name : attribute value }
    #
    #
    # Due to all the Enums, it is recommended to import this file with a wilcard
    #--------------------------------------------------------------------------

    def __init__(self, location, attributes:dict=None):
        self.location = location
        self.user = None
        self.channel = None
        self.flags = set()
        self.__msg_cache = ""
        if attributes != None and isinstance(attributes, dict):
            for k, v in attributes.items():
                if k == ATTRIBUTE.CHANNEL:
                    self.channel = v
                if k == ATTRIBUTE.USER:
                    self.user = v
                if k == ATTRIBUTE.FLAG:
                    self.flags.add(v)

    async def print(self, msg):
        if self.location == OUT.CONSOLE:
            print(msg)
        elif self.location == OUT.DISCORD_PRIVATE_MSG:
            if self.user == None:
                print("no user specified for printing msg: " + msg)
            elif Flag.DEBUG in self.flags:
                print(msg)
            else:
                await self.user.discord_user.send(msg)
        elif self.location == OUT.DISCORD_CHANNEL:
            if Flag.DEBUG in self.flags:
                print(msg)
            else:
                await self.channel.send(msg)

    def print_hold(self, msg):
        self.__msg_cache += msg + "\n"

    async def print_cache(self):
        if len(self.__msg_cache) > 1800:
            await self.print(f"message too long, won't be sent to discord, printing to console...")
            print(self.__msg_cache)
        else:
            if self.location == OUT.CONSOLE:
                await self.print(f"\n{self.__msg_cache}")
            else:
                await self.print(f"```yaml\n{self.__msg_cache}```")
        self.__msg_cache = ""