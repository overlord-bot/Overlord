from array import *
from enum import Enum
from discord.ext import commands
import discord
from .schedule import Schedule

class Flag(Enum):
    MENU_SELECT = 0
    SCHEDULING = 1
    DEBUG = 2
    TEST_RUNNING = 3
    SCHEDULE_SELECTION = 4
    CASE_5 = 5
    SCHEDULE_COURSE_SELECT = 6
    SCHEDULE_COURSE_DELETE = 7

class User():
    
    def __init__(self, discord_user):
        self.discord_user = discord_user
        self.username = str(discord_user)
        self.__schedules = dict() # all schedules this user created <schedule name, Schedule>
        self.curr_schedule = "" # empty string signifies no current schedule

        # temporary variables
        self.__msg_cache = "" # holds a string so it can be outputted at the same time
        self.msg_header = "" # this is added before every msg

        self.flag = set()

        self.schedule_course_search = set()
        self.schedule_course_search_sem = []

    def get_all_schedules(self) -> Schedule:
        return self.__schedules.values()


    def get_schedule(self, schedule_name:str) -> Schedule:
        if schedule_name not in self.__schedules:
            print(f"Schedule {schedule_name} not found")
            return None
        return self.__schedules.get(schedule_name)


    def new_schedule(self, schedule_name:str):
        schedule = Schedule(schedule_name)
        self.__schedules.update({schedule_name : schedule})


    def add_schedule(self, schedule_name:str, schedule:Schedule):
        self.__schedules.update({schedule_name : schedule})


    def get_current_schedule(self):
        return self.get_schedule(self.curr_schedule)


    def rename_schedule(self, old_name:str, new_name:str):
        if old_name not in self.__schedules:
            print(f"Schedule {old_name} not found")
        elif new_name in self.__schedules:
            print(f"Schedule {new_name} already exists, can't change name")
        else:
            self.__schedules.update({new_name : self.__schedules.get(old_name)})
            self.__schedules.pop(old_name)


    '''
    def add_flag(self, flag:Flag, attribute_key=None, attribute_value=None):
        print(f"attribute key {attribute_key}, value {attribute_value}")
        if flag in self.__flags:
            flag_attributes = self.__flags[flag]
            flag_attributes.update({attribute_key:attribute_value})
            self.__flags.update({flag:flag_attributes})
        else:
            self.__flags.update({flag:{attribute_key:attribute_value}})
    '''


    #-----------------------------------------------------------------------
    # Functions to help format and sent messages to the user,
    # it can all be replaced with different UI system later
    #
    # These message methods must be inside the schedule because they hold
    # data over time that's unique for every user.
    #-----------------------------------------------------------------------

    # stores the string inside a cache
    async def msg_hold(self, content:str):
        self.__msg_cache = self.__msg_cache + content + "\n"


    # prints all text within cache into discord's chat
    async def msg_release(self, message:str, fancy:bool=False):
        if Flag.DEBUG in self.flag:
            print(self.__msg_cache)
            self.__msg_cache = ""
        elif len(self.__msg_cache) > 1800:
            await message.channel.send(f"message too long, won't be sent to discord, printing to console...")
            print(self.__msg_cache)
            self.__msg_cache = ""
        elif not fancy:
            await message.channel.send(f"```yaml\n{self.__msg_cache}```")
            self.__msg_cache = ""
        else:
            # embed test
            embed = discord.Embed(title="Slime",color=discord.Color.blue())
            embed.add_field(name="*info*", value=self.__msg_cache, inline = False)
            await message.channel.send(embed=embed)
            self.__msg_cache = ""


    # immediately prints a string to discord's chat
    async def msg(self, message, content:str):
        if Flag.DEBUG in self.flag:
            print(self.msg_header + str(content))
        elif len(content) > 1800:
            await message.channel.send(f"message too long, won't be sent to discord, printing to console...")
            print(self.msg_header + str(content))
            self.__msg_cache = ""
        else:
            await message.channel.send(f"{self.msg_header} {str(content)}")


    # identical to msg(message, content) except this one will print to discord 
    # regardless of debug mode or other checks
    async def force_msg(self, message, content:str):
        if Flag.DEBUG in self.flag:
            print(self.msg_header + str(content))
        await message.channel.send(f"{self.msg_header} {str(content)}")


    def __repr__(self):
        schedule_names = ""
        for s in self.__schedules.keys():
            schedule_names += f"[ {s} ] "
        return f"{str(self.username)}'s schedules: {schedule_names}"


    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self.username == other.username:
            return True
        return False


    def __hash__(self):
        i = 0
        for c in self.username:
            i += ord(c)
        return i
