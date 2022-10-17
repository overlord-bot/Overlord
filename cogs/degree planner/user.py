from array import *
from discord.ext import commands
import discord
import asyncio
import os
import json
from enum import Enum

from .schedule import Schedule


class Flag(Enum):
    MENU_SELECT = 0
    SCHEDULING = 1
    DEBUG = 2
    TEST_RUNNING = 3
    SCHEDULE_SELECTION = 4


class User():
    
    def __init__(self, name:str):
        self.username = name
        self.__schedules = dict() # List of all schedules this person has created <schedule name, Schedule obj>
        self.curr_schedule = "" # empty string signifies no current schedule

         # temporary variables
        self.__msg_cache = "" # holds a string so it can be outputted to discord at the same time to avoid long waits due to network delays when printing individually
        self.msg_header = "" # this is added before every msg, after the [degree planner]

        # flags
        self.flag = set()

    def get_all_schedules(self):
        return self.__schedules.values()


    def get_schedule(self, schedule_name:str):
        if isinstance(self.__schedules.get(schedule_name, ""), str):
            print(f"Schedule {schedule_name} not found")
            return ""
        return self.__schedules.get(schedule_name)


    def new_schedule(self, schedule_name:str):
        schedule = Schedule(schedule_name)
        self.__schedules.update({schedule_name : schedule})


    def add_schedule(self, schedule_name:str, schedule:Schedule):
        self.__schedules.update({schedule_name : schedule})


    def rename_schedule(self, old_name:str, new_name:str):
        if isinstance(self.__schedules.get(old_name, ""), str):
            print(f"Schedule {old_name} not found")
        elif not isinstance(self.__schedules.get(new_name, ""), str):
            print(f"Schedule {new_name} already exists, can't change name")
        else:
            self.__schedules.update({new_name : self.__schedules.get(old_name)})
            self.__schedules.pop(old_name)


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
    async def msg_release(self, message:str, fancy:bool):
        if Flag.DEBUG in self.flag:
            print(self.__msg_cache)
            self.__msg_cache = ""
        elif not fancy:
            await message.channel.send(f"```yaml\n{self.__msg_cache}```")
            self.__msg_cache = ""
        else:
            # little embed test
            embed = discord.Embed(title="Slime",color=discord.Color.blue())
            embed.add_field(name="*info*", value=self.__msg_cache, inline = False)
            await message.channel.send(embed=embed)
            self.__msg_cache = ""


    # immediately prints a string to discord's chat
    async def msg(self, message, content:str):
        if Flag.DEBUG in self.flag:
            print(self.msg_header + str(content))
        else:
            await message.channel.send(f"[Degree Planner] {str(content)}")


    def to_string(self):
        schedule_names = ""
        for s in self.__schedules.keys():
            schedule_names += "[" + s + "] "
        return f"{str(self.username)}'s schedules: {schedule_names}"


    def __eq__(self, other):
        if self.username == other.username:
            return True
        return False


    def __hash__(self):
        return self.username
