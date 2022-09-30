from array import *
from discord.ext import commands
import discord
import asyncio
import os
import json

from .schedule import Schedule


class User():
    
    def __init__(self, name):
        self.username = name
        self.__schedules = dict() # List of all schedules this person has created <schedule name, Schedule obj>

         # temporary variables
        self.__msg_cache = "" # holds a string so it can be outputted to discord at the same time to avoid long waits due to network delays when printing individually

        # flags
        self.selection_flag = False # whether to take user input as a choice for the selection menu
        self.test_running = False # if a test is already running, prevents two tests from running at the same time
        self.debug = False # if set to true, all msg will print to console instead

    def get_all_schedules(self):
        return self.__schedules.values()


    def get_schedule(self, schedule_name):
        if self.__schedules.get(schedule_name, 0) == 0:
            print("Schedule " + schedule_name + " not found")
        return self.__schedules.get(schedule_name, 0)


    def new_schedule(self, schedule_name):
        schedule = Schedule()
        self.__schedules.update({schedule_name : schedule})


    def add_schedule(self, schedule_name, schedule):
        self.__schedules.update({schedule_name : schedule})


    def rename_schedule(self, old_name, new_name):
        if self.__schedules.get(old_name, 0) == 0:
            print("Schedule " + old_name + " not found")
        elif self.__schedules.get(new_name, 0) != 0:
            print("Schedule " + new_name + " already exists, can't change name")
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
    async def msg_hold(self, content):
        self.__msg_cache = self.__msg_cache + content + "\n"


    # prints all text within cache into discord's chat
    async def msg_release(self, message, fancy):
        if self.debug:
            print(self.__msg_cache)
            self.__msg_cache = ""
        elif not fancy:
            await message.channel.send("```yaml\n" + self.__msg_cache + "```")
            self.__msg_cache = ""
        else:
            # little embed test
            embed = discord.Embed(title="Slime",color=discord.Color.blue())
            embed.add_field(name="*info*", value=self.__msg_cache, inline = False)
            await message.channel.send(embed=embed)
            self.__msg_cache = ""


    # immediately prints a string to discord's chat
    async def msg(self, message, content):
        if self.debug:
            print(str(content))
        else:
            await message.channel.send("[Degree Planner] " + str(content))


    def to_string(self):
        schedule_names = ""
        for s in self.__schedules.keys():
            schedule_names += "[" + s + "] "
        return str(self.username) + "'s schedules: " + schedule_names


    def __eq__(self, other):
        if self.username == other.username:
            return True
        return False


    def __hash__(self):
        return self.username
