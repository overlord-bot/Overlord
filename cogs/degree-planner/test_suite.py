import logging

from .course import Course
from .catalog import *
from .degree import Degree
from .rules import Rule
from .schedule import Schedule
from .course_template import Template
from .search import Search
from ..utils.output import *
from .user import *

class Test1():    
    async def test(self, output:Output=None):
        if output == None: output = Output(OUT.CONSOLE)

        await output.print("Generating synthetic test data set")
        user = User("testuser")

        if user.get_schedule("test") == None:
            await output.print("No previous schedule named 'test' exists, creating new test schedule")
            user.new_schedule("test")
        else:
            await output.print("Previously created schedule named 'test' exists, deleting its content...")
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

        assert (course1.display_name == "Data Structures" and course1.major == "CSCI" and course1.course_id == 1200 and
                course1.name == "csci 1200 data structures")
        assert course2.display_name == "Algorithms" and course2.major == "CSCI" and course2.course_id == 2300
        assert course3.display_name == "Circuits" and course3.major == "ECSE" and course3.course_id == 2010
        assert (course4.display_name == "Animation" and course4.major == "ARTS" and course4.course_id == 4070 and 
                "Digital Arts" in course4.HASS_pathway)
        assert (course5.display_name == "Networking in the Linux Kernel" and course5.major == "CSCI" and 
                course5.course_id == 4310 and course5.CI == True and "Systems and Software" in course5.concentration)
        assert (course6.display_name == "Cryptography 1" and course6.major == "CSCI" and course6.course_id == 4230 and 
                course6.CI == True and "Theory, Algorithms and Mathematics" in course6.concentration)

        #------------------------------------------------------------------------------------------
        # Add courses to the a catalog
        #------------------------------------------------------------------------------------------
        await output.print("\nAdding courses to catalog")
        catalog = Catalog()
        catalog.add_course(course1)
        catalog.add_course(course2)
        catalog.add_course(course3)
        catalog.add_course(course4)
        catalog.add_course(course5)
        catalog.add_course(course6)

        output.print_hold("\nPrinting courses:")

        for course in catalog.get_all_courses():
            output.print_hold(str(course))
        await output.print_cache()

        #------------------------------------------------------------------------------------------
        # Add courses to user's schedule
        #------------------------------------------------------------------------------------------
        user.get_schedule("test").add_course(catalog.get_course("csci 1200 data structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("csci 2300 algorithms"), 2)
        user.get_schedule("test").add_course(catalog.get_course("ecse 2010 circuits"), 4)
        user.get_schedule("test").add_course(catalog.get_course("arts 4070 animation"), 4)
        user.get_schedule("test").add_course(catalog.get_course("csci 1200 data structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("csci 1200 data structures"), 1)
        user.get_schedule("test").add_course(catalog.get_course("csci 1200 data structures"), 5)
        user.get_schedule("test").remove_course(catalog.get_course("csci 1200 data structures"), 5)
        user.get_schedule("test").add_course(catalog.get_course("csci 1200 data structures"), 8)
        user.get_schedule("test").add_course(catalog.get_course("csci 4310 networking in the linux kernel"), 8)
        user.get_schedule("test").add_course(catalog.get_course("csci 4230 cryptography 1"), 8)
        user.get_schedule("test").add_course(catalog.get_course("arts 4070 animation"), 0)
        
        #------------------------------------------------------------------------------------------
        # checks to make sure add and remove worked properly
        # no duplicates within one semester but allowing for duplicates across semesters
        #------------------------------------------------------------------------------------------
        await output.print("\nAdded courses to schedule, printing schedule")
        output.print_hold(str(user.get_schedule("test")))
        await output.print_cache()

        assert len(user.get_schedule("test").get_semester(0)) == 1
        assert len(user.get_schedule("test").get_semester(1)) == 1
        assert len(user.get_schedule("test").get_semester(4)) == 2
        assert len(user.get_schedule("test").get_semester(5)) == 0
        assert len(user.get_schedule("test").get_semester(8)) == 3

        #------------------------------------------------------------------------------------------
        # testing course attribute search with get_best_course_match
        #------------------------------------------------------------------------------------------
        await output.print("\nBeginning testing of course attribute search")
        
        course_target1 = Course("", "", 0) # all CI courses
        course_target1.CI = True
        course_target2 = Course("", "", 4000) # all 4000 level courses
        course_target3 = Course("Data Structures", "CSCI", 1200) # data structures
        course_target5 = Course("", "", 0) # all theory concentration courses
        course_target5.concentration.add("Theory, Algorithms and Mathematics")

        bundle1 = catalog.get_best_course_match(course_target1)
        await output.print(f"Bundle1: {str(bundle1)}")
        bundle1_ans = {catalog.get_course("networking in the linux kernel"),catalog.get_course("Cryptography 1")}
        await output.print(f"Bundle1_ans: {str(bundle1_ans)}")
        assert bundle1 == bundle1_ans

        bundle2 = catalog.get_best_course_match(course_target2)
        await output.print(f"Bundle2: {set(bundle2)}")
        bundle2_ans = {course4, course5, course6}
        await output.print(f"Bundle2_ans: {str(bundle2_ans)}")
        assert bundle2 == bundle2_ans

        bundle3 = catalog.get_best_course_match(course_target3)
        bundle3_ans = {course1}
        assert bundle3 == bundle3_ans

        bundle5 = catalog.get_best_course_match(course_target5)
        await output.print(f"Bundle5: {str(bundle5)}")
        bundle5_ans = {course6}
        await output.print(f"Bundle5_ans: {str(bundle5_ans)}")
        assert bundle5 == bundle5_ans

        #------------------------------------------------------------------------------------------
        # testing wildcards with get_course_match()
        #------------------------------------------------------------------------------------------
        await output.print(f"\nBeginning wildcard course matching tests!")

        catalog.add_course(course7)

        template1 = Course("", "", 2000)
        template1ans = {course2,course3}
        await output.print(f"template1response: {str(catalog.get_course_match(template1))}\n" + \
            f"template1ans: {str(template1ans)}")
        assert catalog.get_best_course_match(template1) == template1ans

        template2 = Template("Concentration requirement", Course("", "", 4000))
        template2.template_course.concentration = "*"
        template2ans1 = {course5}
        template2ans2 = {course6, course7}
        await output.print(f"template2response: {str(catalog.get_course_match(template2))}\n" + \
            f"template2ans: course5, course6 course7")
        assert template2ans1 in catalog.get_course_match(template2).values()
        assert template2ans2 in catalog.get_course_match(template2).values()
        assert catalog.get_best_course_match(template2) == template2ans2

        #------------------------------------------------------------------------------------------
        # Rule object testing
        #------------------------------------------------------------------------------------------
        await output.print(f"\nbeginning rules tests!")
        rule1 = Rule("concentration requirement")
        rule1.add_template(template2, 2)
        status_return = rule1.fulfillment(catalog.get_all_courses())
        await output.print(f"status_return of rule fulfillment() method: \n{str(status_return)}")
        status_return2 = rule1.fulfillment_return_message(catalog.get_all_courses())
        await output.print(f"status_return of rule fulfillment_return_message() method: \n{status_return2}")
        
        for i in status_return.values():
            assert template2ans2 in i.values()

        await output.print(f"completed rules tests")

        #------------------------------------------------------------------------------------------
        # Search testing
        #------------------------------------------------------------------------------------------
        await output.print(f"\nbeginning search tests!")
        search = Search(catalog.get_all_course_names())
        assert search.search("dat str") == ["csci 1200 data structures"]

        #------------------------------------------------------------------------------------------
        # Output tests
        #------------------------------------------------------------------------------------------

        # testing json dumps:
        y = json.loads(user.json())
        print('user json dump: \n' + str(y))
        y = json.loads(catalog.json())
        print('catalog json dump: \n' + str(y))
        y = json.loads(user.get_schedule('test').json())
        print('schedule json dump: \n' + str(y))
        y = json.loads(course6.json())
        print('course json dump: \n' + str(y))

        await output.print(f"\nPrinting user data: {str(user)}")

        # resetting master_list and conclude test module
        user.get_schedule("test").master_list_init()