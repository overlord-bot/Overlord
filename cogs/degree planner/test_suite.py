from array import *
from discord.ext import commands
import discord
import asyncio

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .rules import Rules
from .schedule import Schedule

class Test1():    
    async def test(self, message, user):
        await user.msg(message, "Generating synthetic test data set")

        if isinstance(user.get_schedule("test"), str):
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
        course4.HASS_pathway.add("Digital Arts")
        course5 = Course("Networking in the Linux Kernel", "CSCI", 4310)
        course5.CI = True
        course5.concentration.add("Systems and Software")
        course6 = Course("Cryptography 1", "CSCI", 4230)
        course6.CI = True
        course6.concentration.add("Theory, Algorithms and Mathematics")
        course7 = Course("Algorithm Analysis", "CSCI", 4020)
        course7.concentration.add("Theory, Algorithms and Mathematics")

        assert course1.name == "Data Structures" and course1.major == "CSCI" and course1.course_id == 1200
        assert course2.name == "Algorithms" and course2.major == "CSCI" and course2.course_id == 2300
        assert course3.name == "Circuits" and course3.major == "ECSE" and course3.course_id == 2010
        assert course4.name == "Animation" and course4.major == "ARTS" and course4.course_id == 4070 and "Digital Arts" in course4.HASS_pathway
        assert course5.name == "Networking in the Linux Kernel" and course5.major == "CSCI" and course5.course_id == 4310 and course5.CI == True and "Systems and Software" in course5.concentration
        assert course6.name == "Cryptography 1" and course6.major == "CSCI" and course6.course_id == 4230 and course6.CI == True and "Theory, Algorithms and Mathematics" in course6.concentration

        # adding courses to catalog

        await user.msg(message, "Adding courses to catalog")

        catalog = Catalog()

        catalog.add_course(course1)
        catalog.add_course(course2)
        catalog.add_course(course3)
        catalog.add_course(course4)
        catalog.add_course(course5)
        catalog.add_course(course6)

        await user.msg_hold("Printing courses:")

        for course in catalog.get_all_courses():
            await user.msg_hold(course.to_string())
        await user.msg_release(message, False)

        # adding courses to the master list
        
        user.get_schedule("test").add_course(catalog.get_course("Data Structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("Algorithms"), 2)
        user.get_schedule("test").add_course(catalog.get_course("Circuits"), 4)
        user.get_schedule("test").add_course(catalog.get_course("Animation"), 4)
        user.get_schedule("test").add_course(catalog.get_course("Data Structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("Data Structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("Data Structures"), 5)
        user.get_schedule("test").remove_course(catalog.get_course("Data Structures"), 5)
        user.get_schedule("test").add_course(catalog.get_course("Data Structures"), 8)
        user.get_schedule("test").add_course(catalog.get_course("Networking in the Linux Kernel"), 8)
        user.get_schedule("test").add_course(catalog.get_course("Cryptography 1"), 8)

        #reference test
        schedule2 = user.get_schedule("test")
        schedule2.add_course(catalog.get_course("Animation"), 0)
        
        #checks to make sure add and remove worked properly, without duplicates within one semester but allowing for duplicates across semesters
        assert len(user.get_schedule("test").get_semester(0)) == 1
        assert len(user.get_schedule("test").get_semester(1)) == 1
        assert len(user.get_schedule("test").get_semester(4)) == 2
        assert len(user.get_schedule("test").get_semester(5)) == 0
        assert len(user.get_schedule("test").get_semester(8)) == 3

        # print masterlist
        await user.msg(message, "Added courses to schedule, printing schedule")
        await user.msg_hold(user.get_schedule("test").to_string())
        await user.msg_release(message, False)

        # Bundle tests
        await user.msg(message, "Beginning testing of class Bundle")

        bundle1 = Bundle("core CS1", "CSCI", 0)
        bundle1.course_bundle = {course1, course2}
        bundle2 = Bundle("core CS2", "CSCI", 10)
        bundle2.course_bundle = {course2, course1}
        bundle3 = Bundle("A schedule", "ECSE", 0)
        bundle3.course_bundle = {course1, course2, course3}
            
        assert bundle1 == bundle2
        assert bundle1 != bundle3
        assert bundle2 != bundle3

        await user.msg(message, "Bundle assertions successful")

        # testing course attribute search
        await user.msg(message, "Beginning testing of course attribute search")
        course_target1 = Course("Default", "Default", 0) # all CI courses
        course_target1.CI = True
        course_target2 = Course("Default", "Default", 4000) # all 4000 level courses
        course_target3 = Course("Data Structures", "Default", 0) # data structures
        course_target4 = Course("Data Structures", "Default", 2000) # none
        course_target5 = Course("Default", "Default", 0) # all theory concentration courses
        course_target5.concentration.add("Theory, Algorithms and Mathematics")

        bundle1 = catalog.get_course_match(course_target1)
        await user.msg(message, f"Bundle1: {bundle1.to_string()}")
        bundle1_ans = Bundle("CI", "NONE", 1)
        bundle1_ans.add(catalog.get_course("Networking in the Linux Kernel"))
        bundle1_ans.add(catalog.get_course("Cryptography 1"))
        await user.msg(message, f"Bundle1_ans: {bundle1_ans.to_string()}")
        assert bundle1 == bundle1_ans

        bundle2 = catalog.get_course_match(course_target2)
        await user.msg(message, f"Bundle2: {bundle2.to_string()}")
        bundle2_ans = Bundle("4000", "NONE", 2)
        bundle2_ans.course_bundle = [course4, course5, course6]
        await user.msg(message, f"Bundle2_ans: {bundle2_ans.to_string()}")
        assert bundle2 == bundle2_ans

        bundle3 = catalog.get_course_match(course_target3)
        bundle3_ans = Bundle("DS", "NONE", 3)
        bundle3_ans.course_bundle = [course1]
        assert bundle3 == bundle3_ans

        bundle4 = catalog.get_course_match(course_target4)
        bundle4_ans = Bundle("NONE", "NONE", 4)
        assert bundle4 == bundle4_ans

        bundle5 = catalog.get_course_match(course_target5)
        await user.msg(message, f"Bundle5: {bundle5.to_string()}")
        bundle5_ans = Bundle("Theory", "NONE", 5)
        bundle5_ans.course_bundle = [course6]
        await user.msg(message, f"Bundle5_ans: {bundle5_ans.to_string()}")
        assert bundle5 == bundle5_ans
        
        
        # List_and_rules tests
        await user.msg(message, "Beginning testing of class List_and_rules")

        lar1 = Rules()
 
        lar1.course_list = [course1, course2]
        lar1.min_courses = 2
        lar1.min_2000_courses = 1
        lar1.required_courses = [course1]
        assert lar1.fulfilled()

        lar1.course_list = [course1]
        assert not lar1.fulfilled()

        lar1.course_list = [course1, course4]
        assert not lar1.fulfilled()

        lar1.course_list = [course1, course2, course6]
        lar1.min_same_concentration = 2
        assert not lar1.fulfilled()

        lar1.course_list = [course1, course2, course6, course7]
        assert lar1.fulfilled()

        await user.msg(message, "List_and_rules assertions successful")

        await user.msg(message, f"Printing user data: {user.to_string()}")

        # resetting master_list and conclude test module
        user.get_schedule("test").master_list_init()