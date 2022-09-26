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
    
    async def test(self, message, user):
        await user.msg(message, "Generating synthetic test data set")

        if user.get_schedule("test") == 0:
            await user.msg(message, "No previous schedule named 'test' exists, creating new test schedule")
            user.new_schedule("test")
        else:
            await user.msg(message, "Previously created schedule named 'test' exists, deleting its content...")
            user.get_schedule("test").master_list_init()


        # generating courses by configuring it here
        course1 = Course("Data Structures", "CSCI", 1200)
        course2 = Course("Algorithms", "CSCI", 2300)
        course3 = Course("Circuits", "ECSE", 2010)
        course4 = Course("Animation", "ARTS", 4070)

        assert course1.name == "Data Structures" and course1.major == "CSCI" and course1.course_id == 1200
        assert course2.name == "Algorithms" and course2.major == "CSCI" and course2.course_id == 2300
        assert course3.name == "Circuits" and course3.major == "ECSE" and course3.course_id == 2010
        assert course4.name == "Animation" and course4.major == "ARTS" and course4.course_id == 4070

        await user.msg_hold(message, "Printing courses:")

        await user.msg_hold(message, "Course1: " + course1.name + " " + course1.major + " " + str(course1.course_id) + " of level " + str(course1.level()))
        await user.msg_hold(message, "Course2: " + course2.name + " " + course2.major + " " + str(course2.course_id) + " of level " + str(course2.level()))
        await user.msg_hold(message, "Course3: " + course3.name + " " + course3.major + " " + str(course3.course_id) + " of level " + str(course3.level()))
        await user.msg_hold(message, "Course4: " + course4.name + " " + course4.major + " " + str(course4.course_id) + " of level " + str(course4.level()))

        await user.msg_release(message, False)

        user.get_schedule("test").master_list_init()
        # adding courses to the master list
        
        user.get_schedule("test").add_course(course1, 1)
        user.get_schedule("test").add_course(course2, 2)
        user.get_schedule("test").add_course(course3, 4)
        user.get_schedule("test").add_course(course4, 4)
        user.get_schedule("test").add_course(course1, 1)
        user.get_schedule("test").add_course(course1, 1)
        user.get_schedule("test").add_course(course1, 5)
        user.get_schedule("test").remove_course(course1, 5)
        user.get_schedule("test").add_course(course1, 8)

        #reference test
        schedule2 = user.get_schedule("test")
        schedule2.add_course(course4, 0)
        
        #checks to make sure add and remove worked properly, without duplicates within one semester but allowing for duplicates across semesters
        assert len(user.get_schedule("test").master_list[0]) == 1
        assert len(user.get_schedule("test").master_list[1]) == 1
        assert len(user.get_schedule("test").master_list[4]) == 2
        assert len(user.get_schedule("test").master_list[5]) == 0
        assert len(user.get_schedule("test").master_list[8]) == 1

        # print masterlist
        await user.msg(message, "Added courses to schedule, printing schedule")
        await user.msg_hold(message, user.get_schedule("test").to_string())
        await user.msg_release(message, False)

        # Bundle tests
        await user.msg(message, "Beginning testing of class Bundle")

        bundle1 = Bundle("core CS1", "CSCI", 0)
        bundle1.course_bundle = {course1, course2}
        bundle2 = Bundle("core CS2", "CSCI", 10)
        bundle2.course_bundle = {course1, course2}
        bundle3 = Bundle("A schedule", "ECSE", 0)
        bundle3.course_bundle = {course1, course2, course3}
            
        assert bundle1 == bundle2
        assert bundle1 != bundle3
        assert bundle2 != bundle3

        await user.msg(message, "Bundle assertions successful")
        
        
        # List_and_rules tests
        await user.msg(message, "Beginning testing of class List_and_rules")

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

        await user.msg(message, "List_and_rules assertions successful")

        await user.msg(message, "Printing user data: " + user.to_string())

        # resetting master_list and conclude test module
        user.get_schedule("test").master_list_init()
        user.test_running = False