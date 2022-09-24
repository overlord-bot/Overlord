from array import *
from discord.ext import commands
import discord
import asyncio

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .list_and_rules import List_and_rules

class Schedule():
    # SCHEDULE GLOBAL VARIABLES

    # needs to be initialized before every use by calling master_list_init()
    # uses 2D array [semester][course]
    master_list = []

    # temporary variables
    msg_content = "" # holds a string so it can be outputted to discord at the same time to avoid long waits due to network delays when printing individually

    # flags
    selection_flag = False # whether to take user input as a choice for the selection menu
    test_running = False # if a test is already running, prevents two tests from running at the same time

    # Initializes the data structure storing all courses in the schedule, grouped by semester
    async def master_list_init(self):
        print("[Degree Planner Initialization] initializing master_list")
        self.master_list.clear()

        #generates 12 empty lists within master_list. Each list represents a semester, with element 0 representing semester 1 and so on.
        for x in range(0, 12):
            self.master_list.append([])

    #-----------------------------------------------------------------------
    # Functions to help format and sent messages to the user
    # it can all be replaced with different UI system later
    #
    # The reason currently these message methods are inside the schedule
    # is because they hold data over time and therefore must be instigated
    # for every user
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

    # prints student's schedule, uses msg_hold and msg_release functions
    async def print_master_list(self, message):
        count = 0
        await self.msg_hold(message, "")
        for courselist in self.master_list:
            count+=1
            await self.msg_hold(message, "Semester " + str(count) + ":")
            for course in courselist:
                await self.msg_hold(message, "\tCourse info: " + course.name + " " + course.major + " " + str(course.course_id))
        await self.msg_release(message, False)