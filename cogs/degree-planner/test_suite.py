from array import *

from .course import Course
from .catalog import Catalog, get_course_match, get_best_course_match
from .degree import Degree
from .rules import Rule
from .schedule import Schedule
from .course_template import Template
from .search import Search

class Test1():    
    async def test(self, message, user):
        await user.msg(message, "Generating synthetic test data set")

        if user.get_schedule("test") == None:
            await user.msg(message, "No previous schedule named 'test' exists, creating new test schedule")
            user.new_schedule("test")
        else:
            await user.msg(message, "Previously created schedule named 'test' exists, deleting its content...")
            user.get_schedule("test").master_list_init()

        #------------------------------------------------------------------------------------------
        # generating test case courses
        #------------------------------------------------------------------------------------------
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

        assert course1.name == "data structures" and course1.major == "CSCI" and course1.course_id == 1200
        assert course2.name == "algorithms" and course2.major == "CSCI" and course2.course_id == 2300
        assert course3.name == "circuits" and course3.major == "ECSE" and course3.course_id == 2010
        assert (course4.name == "animation" and course4.major == "ARTS" and course4.course_id == 4070 and 
                "Digital Arts" in course4.HASS_pathway)
        assert (course5.name == "networking in the linux kernel" and course5.major == "CSCI" and 
                course5.course_id == 4310 and course5.CI == True and "Systems and Software" in course5.concentration)
        assert (course6.name == "cryptography 1" and course6.major == "CSCI" and course6.course_id == 4230 and 
                course6.CI == True and "Theory, Algorithms and Mathematics" in course6.concentration)

        #------------------------------------------------------------------------------------------
        # Add courses to the a catalog
        #------------------------------------------------------------------------------------------
        await user.msg(message, "\nAdding courses to catalog")
        catalog = Catalog()
        catalog.add_course(course1)
        catalog.add_course(course2)
        catalog.add_course(course3)
        catalog.add_course(course4)
        catalog.add_course(course5)
        catalog.add_course(course6)

        await user.msg_hold("\nPrinting courses:")

        for course in catalog.get_all_courses():
            await user.msg_hold(str(course))
        await user.msg_release(message, False)

        #------------------------------------------------------------------------------------------
        # Add courses to user's schedule
        #------------------------------------------------------------------------------------------
        user.get_schedule("test").add_course(catalog.get_course("data structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("algorithms"), 2)
        user.get_schedule("test").add_course(catalog.get_course("circuits"), 4)
        user.get_schedule("test").add_course(catalog.get_course("animation"), 4)
        user.get_schedule("test").add_course(catalog.get_course("data structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("data structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("data structures"), 5)
        user.get_schedule("test").remove_course(catalog.get_course("data structures"), 5)
        user.get_schedule("test").add_course(catalog.get_course("data structures"), 8)
        user.get_schedule("test").add_course(catalog.get_course("networking in the linux kernel"), 8)
        user.get_schedule("test").add_course(catalog.get_course("cryptography 1"), 8)
        user.get_schedule("test").add_course(catalog.get_course("Animation"), 0)
        
        #------------------------------------------------------------------------------------------
        # checks to make sure add and remove worked properly
        # no duplicates within one semester but allowing for duplicates across semesters
        #------------------------------------------------------------------------------------------
        assert len(user.get_schedule("test").get_semester(0)) == 1
        assert len(user.get_schedule("test").get_semester(1)) == 1
        assert len(user.get_schedule("test").get_semester(4)) == 2
        assert len(user.get_schedule("test").get_semester(5)) == 0
        assert len(user.get_schedule("test").get_semester(8)) == 3

        await user.msg(message, "\nAdded courses to schedule, printing schedule")
        await user.msg_hold(str(user.get_schedule("test")))
        await user.msg_release(message, False)

        #------------------------------------------------------------------------------------------
        # testing course attribute search with get_best_course_match
        #------------------------------------------------------------------------------------------
        await user.msg(message, "\nBeginning testing of course attribute search")
        
        course_target1 = Course("", "", 0) # all CI courses
        course_target1.CI = True
        course_target2 = Course("", "", 4000) # all 4000 level courses
        course_target3 = Course("Data Structures", "", 0) # data structures
        course_target4 = Course("Data Structures", "", 2000) # none
        course_target5 = Course("", "", 0) # all theory concentration courses
        course_target5.concentration.add("Theory, Algorithms and Mathematics")

        bundle1 = catalog.get_best_course_match(course_target1)
        await user.msg(message, f"Bundle1: {str(bundle1)}")
        bundle1_ans = {catalog.get_course("Networking in the Linux Kernel"),catalog.get_course("Cryptography 1")}
        await user.msg(message, f"Bundle1_ans: {str(bundle1_ans)}")
        assert bundle1 == bundle1_ans

        bundle2 = catalog.get_best_course_match(course_target2)
        await user.msg(message, f"Bundle2: {set(bundle2)}")
        bundle2_ans = {course4, course5, course6}
        await user.msg(message, f"Bundle2_ans: {str(bundle2_ans)}")
        assert bundle2 == bundle2_ans

        bundle3 = catalog.get_best_course_match(course_target3)
        bundle3_ans = {course1}
        assert bundle3 == bundle3_ans

        bundle4 = catalog.get_best_course_match(course_target4)
        bundle4_ans = set()
        assert bundle4 == bundle4_ans

        bundle5 = catalog.get_best_course_match(course_target5)
        await user.msg(message, f"Bundle5: {str(bundle5)}")
        bundle5_ans = {course6}
        await user.msg(message, f"Bundle5_ans: {str(bundle5_ans)}")
        assert bundle5 == bundle5_ans

        #------------------------------------------------------------------------------------------
        # testing wildcards with get_course_match()
        #------------------------------------------------------------------------------------------
        await user.msg(message, f"\nBeginning wildcard course matching tests!")

        catalog.add_course(course7)

        template1 = Course("", "", 2000)
        template1ans = {course2,course3}
        await user.msg(message, f"template1response: {str(catalog.get_course_match(template1))}\n" + \
            f"template1ans: {str(template1ans)}")
        assert catalog.get_best_course_match(template1) == template1ans

        template2 = Template("Concentration requirement", Course("", "", 4000))
        template2.template_course.concentration = "*"
        template2ans1 = {course5}
        template2ans2 = {course6, course7}
        await user.msg(message, f"template2response: {str(catalog.get_course_match(template2))}\n" + \
            f"template2ans: course5, course6 course7")
        assert template2ans1 in catalog.get_course_match(template2).values()
        assert template2ans2 in catalog.get_course_match(template2).values()
        assert catalog.get_best_course_match(template2) == template2ans2

        #------------------------------------------------------------------------------------------
        # Rule object testing
        #------------------------------------------------------------------------------------------
        await user.msg(message, f"\nbeginning rules tests!")
        rule1 = Rule("concentration requirement")
        rule1.add_template(template2, 2)
        status_return = rule1.fulfillment(catalog.get_all_courses())
        await user.msg(message, f"status_return of rule fulfillment() method: \n{str(status_return)}")
        status_return2 = rule1.fulfillment_return_message(catalog.get_all_courses())
        await user.msg(message, f"status_return of rule fulfillment_return_message() method: \n{status_return2}")
        
        for i in status_return.values():
            assert template2ans2 in i.values()

        await user.msg(message, f"completed rules tests")

        #------------------------------------------------------------------------------------------
        # Search testing
        #------------------------------------------------------------------------------------------
        await user.msg(message, f"\nbeginning search tests!")
        search = Search(catalog.get_all_courses())
        assert search.search("dat str") == ["data structures"]

        await user.msg(message, f"\nPrinting user data: {str(user)}")

        # resetting master_list and conclude test module
        user.get_schedule("test").master_list_init()