from array import *
from discord.ext import commands
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
    # This function is a temporary text based system to control the bot
    # it can all be replaced with different UI system later
    #-----------------------------------------------------------------------
    async def on_message(self, message):
        if message.content.startswith("dp"):
            await self.msg(message, "hiyaa")
            await self.msg(message, "What would you like to do, " + str(message.author)[0:str(message.author).find('#'):1] + "?")
            await self.msg(message, "input the number in chat:  1: begin test sequence  0: cancel")

            #sets the flag to true so the next input (except for "dp") is treated as a response to the selection menu
            self.selection_flag = True
        
        elif self.selection_flag:
            self.selection_flag = False # resets selection flag
            if message.content.casefold() == "1":
                if self.test_running:
                    await self.msg(message, "Test is already running, please wait for its completion")
                else:
                    self.test_running = True
                    await self.test(message)

            elif message.content.casefold() == "0":
                await self.msg(message, "ok :(")

            elif message.content.casefold() == "69":
                await self.msg(message, "nice")
            else:
                await self.msg(message, "Unknown response, cancelling")

    
    async def test(self, message):
        await self.msg(message, "Generating synthetic test data set")

        # generating courses by configuring it here
        course1 = Course("Data Structures", "CSCI", 1200)
        course2 = Course("Algorithms", "CSCI", 2300)
        course3 = Course("Circuits", "ECSE", 2010)

        assert course1.name == "Data Structures" and course1.major == "CSCI" and course1.id == 1200
        assert course2.name == "Algorithms" and course2.major == "CSCI" and course2.id == 2300
        assert course3.name == "Circuits" and course3.major == "ECSE" and course3.id == 2010

        await self.msg_hold(message, "Courses generated, printing courses")

        await self.msg_hold(message, "Course1: " + course1.name + " " + course1.major + " " + str(course1.id))
        await self.msg_hold(message, "Course2: " + course2.name + " " + course2.major + " " + str(course2.id))
        await self.msg_hold(message, "Course3: " + course3.name + " " + course3.major + " " + str(course3.id))

        await self.msg_release(message)

        await self.master_list_init()

        # adding courses to the master list
        self.master_list[0].append(course1)
        self.master_list[0].append(course2)
        self.master_list[2].append(course3)

        # print masterlist
        await self.msg(message, "Added courses to schedule, printing schedule")
        await self.print_master_list(message)

        # Bundle tests
        await self.msg(message, "Beginning testing of class Bundle")

        bundle1 = Bundle("core CS1", "CSCI", 0)
        bundle1.course_bundle = {course1, course2}
        bundle2 = Bundle("core CS2", "CSCI", 10)
        bundle2.course_bundle = {course1, course2}
        bundle3 = Bundle("A schedule", "ECSE", 0)
        bundle3.course_bundle = {course1, course2, course3}
            
        assert bundle1 == bundle2
        assert bundle1 != bundle3
        assert bundle2 != bundle3

        await self.msg(message, "Bundle assertions successful")

        await self.master_list_init()

        await self.msg(message, "Test completed")
        self.test_running = False



    #-----------------------------------------------------------------------
    # Functions to help format and sent messages to the user
    # it can all be replaced with different UI system later
    #-----------------------------------------------------------------------

    async def msg_hold(self, message, content):
        print("content added" + content)
        self.msg_content = self.msg_content + content + "\n"

    async def msg_release(self, message):
        await message.channel.send("[Degree Planner] " + self.msg_content)
        self.msg_content = ""

    async def msg(self, message, content):
        await message.channel.send("[Degree Planner] " + str(content))
        # print("[Degree Planner] " + str(content))

    async def print_master_list(self, message):
        count = 0
        await self.msg_hold(message, "")
        for courselist in self.master_list:
            count+=1
            await self.msg_hold(message, "  Semester " + str(count) + ":")
            for course in courselist:
                await self.msg_hold(message, "    Course info: " + course.name + " " + course.major + " " + str(course.id))
        await self.msg_release(message)
