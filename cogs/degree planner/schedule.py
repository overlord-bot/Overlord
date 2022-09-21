from array import *
from discord.ext import commands
import asyncio

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .list_and_rules import List_and_rules


class Schedule(commands.Cog, name="Degree Planner"):

    def __init__(self, bot):
        self.bot = bot

    master_list = []
    print("hi")
    for x in range(0, 10):
        master_list.append([])

    test_flag = False

    @commands.Cog.listener()
    async def on_message(self, message):
        global test_flag
        if message.author == self.bot.user or message.author.bot:
            return

        elif message.content.startswith("dp"):
            await self.msg(message, "nya")

            if self.test_flag:
                await self.msg(message, "ERROR 1 IMPOSSIBLE STATE")
            else:
                await self.msg(message, "Begin test sequence?")
                self.test_flag = True

        elif message.content.startswith("yes") and self.test_flag:
            self.test_flag = False
            await self.test(message)

        elif message.content.startswith("no") and self.test_flag:
            self.test_flag = False
            await self.msg(message, "ok :(")

        elif self.test_flag:
            self.test_flag = False
            await self.msg(message, "Unknown response, cancelling")

        else:
            self.test_flag = False

    
    async def test(self, message):
        await self.msg(message, "Generating synthetic test data set")

        course1 = Course("Data Structures", "CSCI", 1200)
        course2 = Course("Algorithms", "CSCI", 2300)
        course3 = Course("Circuits", "ECSE", 2010)

        assert course1.name == "Data Structures" and course1.major == "CSCI" and course1.id == 1200
        assert course2.name == "Algorithms" and course2.major == "CSCI" and course2.id == 2300
        assert course3.name == "Circuits" and course3.major == "ECSE" and course3.id == 2010

        await self.msg(message, "Courses generated, printing courses")

        await self.msg(message, "Course1: " + course1.name + " " + course1.major + " " + str(course1.id))
        await self.msg(message, "Course2: " + course2.name + " " + course2.major + " " + str(course2.id))
        await self.msg(message, "Course3: " + course3.name + " " + course3.major + " " + str(course3.id))

        #adding courses to the master list
        self.master_list[0].append(course1)
        self.master_list[0].append(course2)
        self.master_list[2].append(course3)

        #print masterlist
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


    async def msg(self, message, content):
        await message.channel.send("[Degree Planner] " + str(content))

    async def print_master_list(self, message):
        count = 0
        for courselist in self.master_list:
            count+=1
            await self.msg(message, "  Semester " + str(count) + ":")
            for course in courselist:
                await self.msg(message, "    Course info: " + course.name + " " + course.major + " " + str(course.id))



async def setup(bot):
    await bot.add_cog(Schedule(bot))
