from array import *
from discord.ext import commands
import discord
import asyncio

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .list_and_rules import List_and_rules
from .schedule import Schedule

class Test1():
    # temporary variables
    msg_content = "" # holds a string so it can be outputted to discord at the same time to avoid long waits
    
    async def test(self, message, schedule):
        await schedule.msg(message, "Generating synthetic test data set")
        # generating courses by configuring it here
        course1 = Course("Data Structures", "CSCI", 1200)
        course2 = Course("Algorithms", "CSCI", 2300)
        course3 = Course("Circuits", "ECSE", 2010)
        course4 = Course("Animation", "ARTS", 4070)

        assert course1.name == "Data Structures" and course1.major == "CSCI" and course1.course_id == 1200
        assert course2.name == "Algorithms" and course2.major == "CSCI" and course2.course_id == 2300
        assert course3.name == "Circuits" and course3.major == "ECSE" and course3.course_id == 2010
        assert course4.name == "Animation" and course4.major == "ARTS" and course4.course_id == 4070

        await schedule.msg_hold(message, "Printing courses:")

        await schedule.msg_hold(message, "Course1: " + course1.name + " " + course1.major + " " + str(course1.course_id) + " of level " + str(course1.level()))
        await schedule.msg_hold(message, "Course2: " + course2.name + " " + course2.major + " " + str(course2.course_id) + " of level " + str(course2.level()))
        await schedule.msg_hold(message, "Course3: " + course3.name + " " + course3.major + " " + str(course3.course_id) + " of level " + str(course3.level()))
        await schedule.msg_hold(message, "Course4: " + course4.name + " " + course4.major + " " + str(course4.course_id) + " of level " + str(course4.level()))

        await schedule.msg_release(message, False)

        await schedule.master_list_init()

        # adding courses to the master list
        schedule.master_list[0].append(course1)
        schedule.master_list[0].append(course2)
        schedule.master_list[2].append(course3)
        schedule.master_list[3].append(course4)

        # print masterlist
        await schedule.msg(message, "Added courses to schedule, printing schedule")
        await schedule.print_master_list(message)

        # Bundle tests
        await schedule.msg(message, "Beginning testing of class Bundle")

        bundle1 = Bundle("core CS1", "CSCI", 0)
        bundle1.course_bundle = {course1, course2}
        bundle2 = Bundle("core CS2", "CSCI", 10)
        bundle2.course_bundle = {course1, course2}
        bundle3 = Bundle("A schedule", "ECSE", 0)
        bundle3.course_bundle = {course1, course2, course3}
            
        assert bundle1 == bundle2
        assert bundle1 != bundle3
        assert bundle2 != bundle3

        await schedule.msg(message, "Bundle assertions successful")
        
        
        # List_and_rules tests
        await schedule.msg(message, "Beginning testing of class List_and_rules")

        lar1 = List_and_rules()
        lar1.course_list = [course1, course2]
        lar1.min_courses = 2
        lar1.min_2000_courses = 1
        lar1.required_courses = [course1]
        assert lar1.fulfilled()

        lar1.course_list = [course1]
        assert not lar1.fulfilled()

        lar1.course_list = [course1, course4]
        assert not lar1.fulfilled()

        await schedule.msg(message, "List_and_rules assertions successful")

        # resetting master_list and conclude test module
        await schedule.master_list_init()
        schedule.test_running = False