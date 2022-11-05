from array import *
from discord.ext import commands
import discord
import asyncio
import json
import os
import random

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .rules import Rule
from .schedule import Schedule
from .test_suite import Test1
from .user import User
from .user import Flag
from .search import Search
from .course_template import Template
from .output import Output
from .output import OUT


#########################################################################
#                            IMPORTANT NOTE:                            #
#                                                                       #
# This class is created once and is not instigated for each user.       #
# It is essential to keep all user specific data, such as input flags   #
# (i.e. flag.MENU_SELECT) or message delivery methods (i.e. msg())      #
# inside the User class, which is instigated for each user.             #
#########################################################################


class Degree_Planner(commands.Cog, name="Degree Planner"):

    def __init__(self, bot):
        self.bot = bot

        # each user is assigned a User object and stored in this dictionary
        # Users = <discord user id, User>
        self.users = dict()
        self.catalog = Catalog()
        self.course_search = Search()

        self.flags = set()

        # just to help keep track of deployed versions without needing access to host
        self.VERSION = "dev 10.1 (working fulfillment checker)" 
    
    
    #--------------------------------------------------------------------------
    # Main message listener
    #
    # passes the message content to a helper function which will 
    # read the message and determine responses.
    #--------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):

        # ignore messages not from users
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            if message.author.id in self.users:
                print(f"received msg from returning user: {message.author}; " + \
                    f"user id: {message.author.id}")
                await self.message_handler(message)
            else:
                print(f"received msg from new user: {message.author}; " + \
                    f"user id: {message.author.id}")
                user = User(message.author)
                self.users.update({message.author.id:user})
                await self.message_handler(message)

        print(f"end of message handler function")


    #--------------------------------------------------------------------------
    # This function is a text based system to control the degree planner
    # it can be replaced with different UI system later
    #--------------------------------------------------------------------------
    async def message_handler(self, message):
        user:User = self.users.get(message.author.id)
        msg = message.content
        output = Output(OUT.DISCORD_CHANNEL, {"channel":message.channel})
        output_debug = Output(OUT.CONSOLE)

        if Flag.TEST_RUNNING in self.flags:
            await output.print("Test running, please try again later")
            return

        # if we receive a command in the format !dp <arg>
        if (msg.casefold().startswith("!dp") and len(msg.split(' ')) == 2):
            # simulates as if the user typed in !dp and <int> separately
            user.flag.add(Flag.MENU_SELECT)
            # changes msg to be the !dp number
            msg = msg.split(' ')[1]

        # main menu command
        if msg.casefold() == "!dp":
            # prints "what would you like to do, <username without tag>?"
            await output.print(f"Hiyaa, what would you like to do, " + \
                f"{str(message.author)[0:str(message.author).find('#'):1]}?") 
            await output.print("Please input a number in chat:  " + \
                "1: begin test sequence " + \
                "2: import courses from json file " + \
                "9: run scheduler " + \
                "0: cancel")
            await output.print(f"Degree Planner version: {self.VERSION}")

            user.flag.add(Flag.MENU_SELECT)
            return
        
        #----------------------------------------------------------------------
        # main menu command !dp argument cases:
        #----------------------------------------------------------------------
        if Flag.MENU_SELECT in user.flag:
            user.flag.remove(Flag.MENU_SELECT)

            # CASE 1: run test suite
            if msg.casefold() == "1":
                output_debug.print("INPUT 1 REGISTERED")
                self.flags.add(Flag.TEST_RUNNING)
                output_debug.print("BEGINNING TEST")
                await self.test(message)
                output_debug.print("FINISHED TEST")
                output.print("Test completed successfully, all assertions met")
                self.flags.remove(Flag.TEST_RUNNING)
                return

            # CASE 2: run data fetch from json
            # this will load both courses and degrees
            elif msg.casefold() == "2":
                output_debug.print("INPUT 2 REGISTERED")
                self.parse_data()
                
                return

            #CASE 5: Search course (TEMPORARY TESTING PURPOSES)
            elif msg.casefold() == "5":
                print("INPUT 5 REGISTERED")
                await output.print(message, "Enter the course")
                user.flag.add(Flag.CASE_5)
                return

            # CASE 9: Begin actual scheduler, the main feature of this program
            elif msg.casefold() == "9":
                print("INPUT 9 REGISTERED")
                user.flag.add(Flag.SCHEDULING)
                user.flag.add(Flag.SCHEDULE_SELECTION)
                await output.print("You are now in scheduling mode!")
                await output.print("Enter the name of the schedule to modify. " + \
                    "If the schedule entered doesn't exist, it will be created")
                return

            # CASE 0: cancel selection operation
            elif msg.casefold() == "0":
                await output.print("ok :(")
                return

            # CASE 69: nice
            elif msg.casefold() == "69":
                await output.print("nice")
                return

            else:
                await output.print("Unknown response, cancelling")
                return

        #----------------------------------------------------------------------
        # course scheduling mode, the feature intended to be used in the end
        #----------------------------------------------------------------------
        if Flag.SCHEDULING in user.flag:

            command_raw = msg.split(",") # user input split up, will parse as a command
            command = [e.strip().casefold() for e in command_raw] # strips and lowercases all args
            command = [e for e in command if e] # removes empty strings from list
            output_debug.print("Inputted scheduling command: " + str(command))
            cmd = command[0] # command str will be modified later, this assignment is necessary!
            l = len(command) # command str will be modified later, this assignment is necessary!

            current_schedule = user.get_schedule(user.curr_schedule)

            if not l:
                await output.print("no command detected")
                return

            # sets the current schedule to modify
            if Flag.SCHEDULE_SELECTION in user.flag:
                cmd = cmd.casefold()
                schedule = user.get_schedule(cmd)
                if schedule == None:
                    await output.print(f"Schedule {cmd} not found, generating new one!")
                    user.new_schedule(cmd)
                    user.curr_schedule = cmd
                else:
                    await output.print(f"Successfully switched to schedule {cmd}!")
                    user.curr_schedule = cmd
                user.flag.remove(Flag.SCHEDULE_SELECTION)
                return

            # user currently selecting a course from a list of choices to add to schedule
            if Flag.SCHEDULE_COURSE_SELECT in user.flag:
                courses = user.schedule_course_search
                if not cmd.isdigit():
                    await output.print("Please enter a number")
                    return
                num_select = int(cmd)
                if num_select not in range(1, len(courses) + 1):
                    await output.print("Please enter a valid selection number")
                    return
                course = courses[num_select - 1]
                command = ["add", user.schedule_course_search_sem, course.name]
                cmd = command[0]
                l = 3
                user.flag.remove(Flag.SCHEDULE_COURSE_SELECT)
                
            # user currently selecting a course froma list of choices to remove from schedule
            if Flag.SCHEDULE_COURSE_DELETE in user.flag:
                courses = user.schedule_course_search
                if not cmd.isdigit():
                    await output.print("Please enter a number")
                    return
                num_select = int(cmd)
                if num_select not in range(1, len(courses) + 1):
                    await output.print("Please enter a valid selection number")
                    return
                course = courses[num_select - 1]
                command = ["remove", user.schedule_course_search_sem, course.name]
                cmd = command[0]
                l = 3
                user.flag.remove(Flag.SCHEDULE_COURSE_DELETE)

            # user initiates process to add course to schedule
            if cmd == "add":
                command.pop(0)
                if l < 3:
                    await output.print("Not enough arguments")
                    return
                semester = int(command.pop(0))
                if semester not in range(0, current_schedule.SEMESTERS_MAX):
                    await output.print("Invalid semester, enter number between 0 and 11")
                    return

                for course_name in command:
                    returned_courses = self.course_search.search(course_name)
                    returned_courses = [self.catalog.get_course(c) for c in returned_courses]
                    if len(returned_courses) == 0:
                        await output.print(f"Course {course_name} not found")
                        continue
                    elif len(returned_courses) == 1:
                        course = returned_courses[0]
                    else:
                        await output.print(f"query {course_name} has multiple valid courses, please choose from list:")
                        i = 1
                        for c in returned_courses:
                            output.print_hold(f"{i}: {repr(c)}")
                            i += 1
                        await output.print_cache()
                        user.flag.add(Flag.SCHEDULE_COURSE_SELECT)
                        user.schedule_course_search = returned_courses
                        user.schedule_course_search_sem = semester
                        continue

                    if course == None:
                        await output.print(f"Course {course_name} not found")
                        continue

                    current_schedule.add_course(course, semester)
                    await output.print(f"Added course {course.name} to semester {semester}")
                    
            # user intiates process to remove course from schedule
            elif cmd == "remove":
                command.pop(0)
                if l < 3:
                    await output.print("Not enough arguments")
                    return
                semester = int(command.pop(0))
                if semester not in range(0, current_schedule.SEMESTERS_MAX):
                    await output.print("Invalid semester, enter number between 0 and 11")
                    return
                this_semester_courses = current_schedule.get_semester(semester)
                if not len(this_semester_courses):
                    await output.print(f"No courses in semester {semester}")
                    return

                semester_course_search = Search(this_semester_courses, True)

                for course_name in command:
                    returned_courses = semester_course_search.search(course_name)
                    returned_courses = [self.catalog.get_course(c) for c in returned_courses]
                    if len(returned_courses) == 0:
                        await output.print(f"Course {course_name} not found")
                        continue
                    elif len(returned_courses) == 1:
                        course = returned_courses[0]
                    else:
                        await output.print(f"query {course_name} has multiple valid courses, please choose from list:")
                        i = 1
                        for c in returned_courses:
                            output.print_hold(f"{i}: {repr(c)}")
                            i += 1
                        await output.print_cache()
                        user.flag.add(Flag.SCHEDULE_COURSE_DELETE)
                        user.schedule_course_search = returned_courses
                        user.schedule_course_search_sem = semester
                        continue

                    if course == None or course not in current_schedule.get_semester(semester):
                        await output.print(f"Can't find course {course_name} in semester {semester}")
                        continue
                    current_schedule.remove_course(course, semester)
                    await output.print(f"Removed course {course.name} from semester {semester}")

            elif cmd == "print":
                output.print_hold(str(current_schedule))
                await output.print_cache()

            # sets degree of user, replaces previous selection
            elif cmd == "degree":
                command.pop(0)
                if l != 2:
                    await output.print("incorrect amount of arguments, " + \
                        "use degree,<degree name> to set your schedule's degree")
                else:
                    degree = self.catalog.get_degree(command[0])
                    if degree == None:
                        await output.print(f"invalid degree entered: {command[0]}")
                        return
                    user.get_current_schedule().degree = degree
                    await output.print(f"set your degree to {degree.name}")

            # displays fulfillment status of current degree
            elif cmd == "fulfillment":
                if user.get_current_schedule().degree == None:
                    await output.print("no degree specified")
                else:
                    output.print_hold(user.get_current_schedule().
                        degree.fulfillment_msg(user.get_current_schedule().get_all_courses()))
                    await output.print_cache()

            # change the current schedule to modify
            elif cmd == "reschedule":
                await output.print("Understood, please enter schedule name to modify:")
                user.flag.add(Flag.SCHEDULE_SELECTION)

            # exits from scheduling mode
            elif cmd == "exit":
                await output.print("Exiting scheduling mode")
                user.flag.remove(Flag.SCHEDULING)

            else:
                await output.print("Unrecognized action")

        #----------------------------------------------------------------------
        # case 5 is a temporary test case for the search function in search.py
        #----------------------------------------------------------------------
        elif Flag.CASE_5 in user.flag:
            user.flag.remove(Flag.CASE_5)
            possible_courses = self.course_search.search(message.content.casefold())
            await output.print("possible courses: " + str(possible_courses))


    #--------------------------------------------------------------------------
    # HELPER FUNCTIONS FOR THE TEXT UI
    #--------------------------------------------------------------------------

    # Helper function that starts running the test_suite, can be replaced
    # by pytest later
    async def test(self, output:Output=Output(OUT.CONSOLE)):
        test_suite = Test1()
        output.flags.add(Flag.DEBUG)
        await test_suite.test(output)
        output.flags.remove(Flag.DEBUG)   

    
    async def parse_data(self, output:Output=Output(OUT.CONSOLE)):
        output.flags.add(Flag.DEBUG)
        # redirects user messages into terminal, too much data for discord chat

        catalog_file = "catalog_results.json"
        degree_file = "class_results.json"

        await self.parse_courses(catalog_file, output)
        await output.print("Sucessfully parsed catalog data")
        
        # set up searcher for finding courses based on incomplete user input
        self.course_search.update_items(self.catalog.get_all_course_names())
        self.course_search.generate_index()

        await self.parse_degrees(degree_file, output)
        await output.print("Sucessfully parsed degree data, printing catalog")
        output.print_hold(str(self.catalog))
        await output.print_cache()
        await output.print("parsing completed")

        output.flags.remove(Flag.DEBUG)


    #--------------------------------------------------------------------------
    # parses json data of format [{course attribute : value}] 
    # into a set of Course objects stored in Catalog
    #--------------------------------------------------------------------------
    async def parse_courses(self, file_name, output:Output=Output(OUT.CONSOLE)):
        
        # will not parse if the test is running to prevent data loss since Catalog is shared
        # note that running a test will destroy all data within the Catalog, 
        # so rerunning this method is necessary after a test
        if Flag.TEST_RUNNING in self.flags:
            await output.print("Operation unavailable due to another user operation running")
            return
        await output.print("Beginning parsing course data into catalog")

        # There are 4 locations for catalog_results and class_results, checked in this order:
        # 1) /cogs/webcrawling/
        # 2) /cogs/degree-planner/data/
        # 3) /cogs/degree-planner/
        # 4) / (root directory of bot)
        if os.path.isfile(os.getcwd() + "/cogs/webcrawling/" + file_name):
            await output.print(f"file found: {os.getcwd()}/cogs/webcrawling/" + file_name)
            file_catalog_results = open(os.getcwd() + "/cogs/webcrawling/" + file_name)
        elif os.path.isfile(os.getcwd() + "/cogs/degree-planner/data/" + file_name):
            await output.print(f"file found: {os.getcwd()}/cogs/degree-planner/data/" + file_name)
            file_catalog_results = open(os.getcwd() + "/cogs/degree-planner/data/" + file_name)
        elif os.path.isfile(os.getcwd() + "/cogs/degree-planner/" + file_name):
            await output.print(f"file found: {os.getcwd()}/cogs/degree-planner/" + file_name)
            file_catalog_results = open(os.getcwd() + "/cogs/degree-planner/" + file_name)
        elif os.path.isfile(os.getcwd() + "/" + file_name):
            await output.print(f"file found: {os.getcwd()}/" + file_name)
            file_catalog_results = open(os.getcwd() + "/" + file_name)
        else:
            await output.print("catalog file not found")
            return

        json_data = json.load(file_catalog_results)
        file_catalog_results.close()
        #----------------------------------------------------------------------

        #----------------------------------------------------------------------
        # Begin iterating through every dictionary stored inside the json_data
        #
        # json data format: list of dictionaries with each dictionary representing 
        # a single course and its data
        #----------------------------------------------------------------------
        for element in json_data:

            if 'course_name' in element and 'course_subject' in element and 'course_number' in element:
                course = Course(element['course_name'], element['course_subject'], element['course_number'])
            else:
                print("PARSING ERROR: course name, subject or number not found " + str(element))
                continue

            if 'course_credit_hours' in element:
                course.credits = element['course_credit_hours']
            
            if 'course_is_ci' in element:
                course.CI = element['course_is_ci']

            if 'HASS_pathway' in element:
                HASS_pathway = element['HASS_pathway'] # list of pathways
                if isinstance(HASS_pathway, list):
                    for pathway in HASS_pathway: # add each individual pathway (stripped of whitespace)
                        course.add_pathway(pathway.strip())
                elif HASS_pathway != "":
                    course.add_pathway(HASS_pathway.strip())

            if 'concentration' in element:
                concentration = element['concentration']
                if isinstance(concentration, list):
                    for con in concentration:
                        course.add_concentration(con.strip())
                elif concentration != "":
                    course.add_concentration(concentration.strip())

            if 'course_requisites' in element:
                prereqs = element['course_requisites']
                if isinstance(prereqs, list):
                    for prereq in prereqs:
                        course.add_prerequisite(prereq.strip())
                elif prereqs != "":
                    course.add_prerequisite(prereqs.strip())

            if 'course_crosslisted' in element:
                cross_listed = element['course_crosslisted']
                if isinstance(cross_listed, list):
                    for cross in cross_listed:
                        course.add_cross_listed(cross.strip())
                elif cross_listed != "":
                    course.add_cross_listed(cross_listed.strip())

            if 'restricted' in element:
                course.restricted = element['restricted']

            if 'course_description' in element:
                course.description = element['course_description']

            self.catalog.add_course(course)


    #--------------------------------------------------------------------------
    # parses degree info from json into Degree objects, and then
    # stored inside the Catalog
    #--------------------------------------------------------------------------
    async def parse_degrees(self, file_name, output:Output=Output(OUT.CONSOLE)):

        # will not parse if the test is running to prevent data loss since Catalog is shared
        # note that running a test will destroy all data within the Catalog, 
        # so rerunning this method is necessary after a test
        if Flag.TEST_RUNNING in self.flags:
            await output.print("Operation unavailable due to another user operation running")
            return
        await output.print("Beginning parsing degree data into catalog")

        if os.path.isfile(os.getcwd() + "/cogs/webcrawling/" + file_name):
            await output.print(f"file found: {os.getcwd()}/cogs/webcrawling/" + file_name)
            file_degree_results = open(os.getcwd() + "/cogs/webcrawling/" + file_name)
        elif os.path.isfile(os.getcwd() + "/cogs/degree-planner/data/" + file_name):
            await output.print(f"file found: {os.getcwd()}/cogs/degree-planner/data/" + file_name)
            file_degree_results = open(os.getcwd() + "/cogs/degree-planner/data/" + file_name)
        elif os.path.isfile(os.getcwd() + "/cogs/degree-planner/" + file_name):
            await output.print(f"file found: {os.getcwd()}/cogs/degree-planner/" + file_name)
            file_degree_results = open(os.getcwd() + "/cogs/degree-planner/" + file_name)
        elif os.path.isfile(os.getcwd() + "/" + file_name):
            await output.print(f"file found: {os.getcwd()}/" + file_name)
            file_degree_results = open(os.getcwd() + "/" + file_name)
        else:
            await output.print("degree file not found")
            return

        json_data = json.load(file_degree_results)
        file_degree_results.close()

        # TESTING DEGREES FOR NOW:
        degree = Degree("computer science")

        rule = Rule("concentration")

        template1 = Template("concentration requirement", Course("", "", 4000))
        template1.template_course.concentration = "*"

        template2 = Template("intensity requirement", Course("", "", 4000))

        template3 = Template("data structures", Course("data structures", "", 0))

        rule.add_template(template1, 2)
        rule.add_template(template2, 3)
        rule.add_template(template3)

        degree.add_rule(rule)
        self.catalog.add_degree(degree)

        output.print(f"added degree {str(degree)} containing rule {str(rule)} to catalog")

        '''
        #----------------------------------------------------------------------
        # Iterating through 'class_results.json', storing data on the core and
        # elective information of each major
        #
        # note that further information describing all aspects of degrees are
        # still needed, potentially in the form of manually created course
        # templates.
        #
        # json data format: { degree name : [ { course attribute : value } ] }
        #----------------------------------------------------------------------
        for degree_name, degree_data in json_data.items():
            degree = Degree(degree_name)
            required_courses = set()

            for requirement in degree_data:
                if requirement['type'] == 'course':
                    required_courses.add(self.catalog.get_course(requirement['name']))
                elif requirement['type'] == 'elective':
                    pass
                '''

async def setup(bot):
    await bot.add_cog(Degree_Planner(bot))
