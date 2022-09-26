from array import *
from discord.ext import commands
import discord
import asyncio
import os
import json

from .schedule import Schedule


class User():

    username = ""
    schedules = dict() # List of all schedules this person has created <schedule name, Schedule obj>
    
    # temporary variables
    msg_content = "" # holds a string so it can be outputted to discord at the same time to avoid long waits due to network delays when printing individually

    # flags
    selection_flag = False # whether to take user input as a choice for the selection menu
    test_running = False # if a test is already running, prevents two tests from running at the same time

    def __init__(self, name):
        self.username = name
    

    def get_all_schedules(self):
        return self.schedules.values()


    def get_schedule(self, schedule_name):
        if self.schedules.get(schedule_name, 0) == 0:
            print("Schedule " + schedule_name + " not found")
        return self.schedules.get(schedule_name, 0)


    def new_schedule(self, schedule_name):
        schedule = Schedule()
        self.schedules.update({schedule_name : schedule})


    def add_schedule(self, schedule_name, schedule):
        self.schedules.update({schedule_name : schedule})


    def rename_schedule(self, old_name, new_name):
        if self.schedules.get(old_name, 0) == 0:
            print("Schedule " + old_name + " not found")
        elif self.schedules.get(new_name, 0) != 0:
            print("Schedule " + new_name + " already exists, can't change name")
        else:
            self.schedules.update({new_name : self.schedules.get(old_name)})
            self.schedules.pop(old_name)


    #-----------------------------------------------------------------------
    # Functions to help format and sent messages to the user,
    # it can all be replaced with different UI system later
    #
    # These message methods must be inside the schedule because they hold
    # data over time that's unique for every user.
    #-----------------------------------------------------------------------

    # stores the string inside a cache
    async def msg_hold(self, message, content):
        print("content added" + content)
        self.msg_content = self.msg_content + content + "\n"


    # prints all text within cache into discord's chat
    async def msg_release(self, message, embedded):
        if embedded:
            # little embed test
            embed = discord.Embed(title="Slime",color=discord.Color.blue())
            embed.add_field(name="*info*", value=self.msg_content, inline = False)
            await message.channel.send(embed=embed)
            self.msg_content = ""
        else:
            # code block test
            await message.channel.send("```yaml\n" + self.msg_content + "```")
            self.msg_content = ""


    # immediately prints a string to discord's chat
    async def msg(self, message, content):
        await message.channel.send("[Degree Planner] " + str(content))


    def to_string(self):
        schedule_names = ""
        for s in self.schedules.keys():
            schedule_names += "[" + s + "] "
        return str(self.username) + "'s schedules: " + schedule_names


    def __eq__(self, other):
        if self.username == other.username:
            return True
        return False


    def __hash__(self):
        return self.username
