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
from .output import *


#########################################################################
#                            IMPORTANT NOTE:                            #
#                                                                       #
# This class is created once and is not instigated for each user.       #
# It is essential to keep all user specific data, such as input flags   #
# (i.e. flag.MENU_SELECT) inside the User class, which is instigated    #
# for each user.                                                        #
#########################################################################


class Degree_Planner(commands.Cog, name="Degree Planner"):

    def __init__(self, bot):
        self.bot = bot

        # each user is assigned a User object and stored in this dictionary
        # Users = <user id, User>

        # note that the User object is meant to represent any user and does not
        # specifically have to be a discord user. It can be generated as long as 
        # a unique user ID is provided in the form of a string.
        self.users = dict()
        self.catalog = Catalog()
        self.course_search = Search()
        self.flags = set()
        
        # just to help keep track of deployed versions without needing access to host
        self.VERSION = "dev 10.1 (working fulfillment checker)" 


    #--------------------------------------------------------------------------
    # Main message listener
    #
    # passes the message content to a helper functions.
    #--------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        # ignore messages not from users
        if message.author == self.bot.user or message.author.bot:
            return

        userid = str(message.author.id)
        if userid in self.users:
            user = self.users[userid]
            print(f"received msg from returning user: {message.author}, user id: {userid}")
        else:
            user = User(userid)
            self.users.update({userid:user})
            print(f"received msg from new user: {message.author}, user id: {userid}")

        output = Output(OUT.DISCORD_CHANNEL, {ATTRIBUTE.CHANNEL:message.channel})
        await self.message_handler(user, message.content, output)


    #--------------------------------------------------------------------------
    # handles message locks and user input control
    #
    # IMPORTANT: this method should be called for all input purposes 
    # rather than input_handler
    #--------------------------------------------------------------------------
    async def message_handler(self, user:User, msg:str, output:Output=Output(OUT.CONSOLE)):
        # we shouldn't be able to run commands while there are other commands in the queue
        if user.command_cache_locked:
            await output.print("please hold on for next command!")
            return
        user.command_cache_locked = True
        await self.input_handler(user, msg, output)


    # parser for input and executes commands
    async def input_handler(self, user:User, msg:str, output:Output=Output(OUT.CONSOLE)):
        output_debug = Output(OUT.CONSOLE)

        if Flag.TEST_RUNNING in self.flags:
            await output.print("Test running, please try again later")
            user.command_cache_locked = False
            return
        #----------------------------------------------------------------------
        # !dp parsing
        #----------------------------------------------------------------------
        # if we receive a command in the format !dp <arg>
        if len(msg.split(' ')) == 2 and msg.split(' ')[0] == "!dp":
            # simulates as if the user typed in !dp and <int> separately
            user.flag.add(Flag.MENU_SELECT)
            msg = msg.split(' ')[1] # changes msg to be the !dp number

        # main menu command
        if msg.casefold() == "!dp":
            await output.print(f"Hiyaa, what would you like to do, {user.username}?")
            output.print_hold("Please input a number in chat:\n" + \
                "  1: begin test sequence \n" + \
                "  2: import courses from json file \n" + \
                "  5: search for course \n" + \
                "  9: run scheduler \n" + \
                "  0: cancel \n")
            output.print_hold(f"Degree Planner version: {self.VERSION}")
            await output.print_cache()
            user.flag.add(Flag.MENU_SELECT)
            user.command_cache_locked = False
            return
        
        #----------------------------------------------------------------------
        # main menu command !dp argument cases:
        #----------------------------------------------------------------------
        if Flag.MENU_SELECT in user.flag:
            user.flag.remove(Flag.MENU_SELECT)
            user.command_cache_locked = False

            # CASE 1: run test suite
            if msg.casefold() == "1":
                await output_debug.print("DP 1 REGISTERED")
                self.flags.add(Flag.TEST_RUNNING)
                await output_debug.print("BEGINNING TEST")
                await self.test(output_debug)
                await output_debug.print("FINISHED TEST")
                await output.print("Test completed successfully, all assertions met")
                self.flags.remove(Flag.TEST_RUNNING)
                return

            # CASE 2: run data fetch from json
            # this will load both courses and degrees
            elif msg.casefold() == "2":
                await output_debug.print("DP 2 REGISTERED")
                await self.parse_data()
                await output.print("parsing completed")
                return

            #CASE 5: Search course (TEMPORARY TESTING PURPOSES)
            elif msg.casefold() == "5":
                await output_debug.print("DP 5 REGISTERED")
                await output.print("Enter the course to search for:")
                user.flag.add(Flag.CASE_5)
                return

            # CASE 9: Begin actual scheduler, the main feature of this program
            elif msg.casefold() == "9":
                await output_debug.print("DP 9 REGISTERED")
                user.flag.add(Flag.SCHEDULING)
                await output.print("You are now in scheduling mode!")
                await output.print("Generated empty schedule 'default'")
                msg = "reschedule, default"

            # CASE 0: cancel selection operation
            elif msg.casefold() == "0":
                await output.print("ok :(")
                return

            # CASE 69: nice
            elif msg.casefold() == "69":
                await output.print("nice")
                return

            else:
                await output.print("Unknown input")
                return

        #----------------------------------------------------------------------
        # course scheduling mode, the feature intended to be used in the end
        #----------------------------------------------------------------------
        if Flag.SCHEDULING in user.flag:

            # strips + casefold args, removes empty strings
            input = msg.strip().casefold()
            command = user.command_cache
            user.command_cache = []
            schedule = user.get_schedule(user.curr_schedule)
            print("cached command:" + str(command))

            # if we are awaiting a response to fix the next element in the command
            if Flag.SCHEDULE_COURSE_SELECT in user.flag:
                courses = user.schedule_course_search
                if not input.isdigit() or int(input) not in range(1, len(courses) + 1):
                    await output.print("Please enter a valid selection number")
                    user.command_cache = command
                    user.command_cache_locked = False
                    return
                course:Course = courses[int(input) - 1]
                command[2] = course.name
                user.flag.remove(Flag.SCHEDULE_COURSE_SELECT)

            # meaning we weren't awaiting a response and that this was a command
            else:
                command += [e.strip().casefold() for e in msg.split(",") if e.strip()]
                print("command: " + str(command))

            if len(command) == 0:
                await output.print("no command detected")
                user.command_cache_locked = False
                return

            cmd = command.pop(0)

            # user initiates process to add or delete course to schedule
            if cmd == "add" or cmd == "remove":
                if len(command) < 2:
                    await output.print("Not enough arguments")
                    user.command_cache_locked = False
                    return
                semester = int(command.pop(0))
                if semester not in range(0, schedule.SEMESTERS_MAX):
                    await output.print("Invalid semester, enter number between 0 and 11")
                    user.command_cache_locked = False
                    return
                # iterate over all courses provided in command
                # if we meet one with multiple possibilities then iteration will stop
                while command:
                    course = command[0]
                    if cmd == "add":
                        cont = await self.add_course(user, course, semester, output)
                    else:
                        cont = await self.remove_course(user, course, semester, output)
                    if cont:
                        user.command_cache = [cmd, semester] + command
                        user.command_cache_locked = False
                        return
                    command.pop(0)

            # prints semester table to output
            elif cmd == "print":
                output.print_hold(str(schedule))
                await output.print_cache()

            # sets degree of user, replaces previous selection
            elif cmd == "degree":
                if not command:
                    await output.print("no arguments found, " + \
                        "use degree,<degree name> to set your schedule's degree")
                    user.command_cache_locked = False
                    return
                else:
                    input = command.pop(0)
                    degree = self.catalog.get_degree(input)
                    if degree == None:
                        await output.print(f"invalid degree entered: {input}")
                    else:
                        user.get_current_schedule().degree = degree
                        await output.print(f"set your degree to {degree.name}")

            # displays fulfillment status of current degree
            elif cmd == "fulfillment":
                if user.get_current_schedule().degree == None:
                    await output.print("no degree specified")
                else:
                    output.print_hold(user.get_current_schedule().degree.
                        fulfillment_msg(user.get_current_schedule().get_all_courses()))
                    await output.print_cache()

            # change the current schedule to modify
            elif cmd == "reschedule":
                if not command:
                    await output.print("invalid command, please use reschedule, <schedule name>")
                    user.command_cache_locked = False
                    return
                schedule_name = command.pop(0).casefold()
                schedule = user.get_schedule(schedule_name)
                if schedule == None:
                    await output.print(f"Schedule {schedule_name} not found, generating new one!")
                    user.new_schedule(schedule_name)
                    user.curr_schedule = schedule_name
                else:
                    await output.print(f"Successfully switched to schedule {schedule_name}!")
                    user.curr_schedule = schedule_name                

            # exits from scheduling mode
            elif cmd == "exit":
                await output.print("Exiting scheduling mode")
                user.flag.remove(Flag.SCHEDULING)
                user.command_cache = []
                user.command_cache_locked = False
                return

            else:
                await output.print("invalid command")
                user.command_cache = []
                user.command_cache_locked = False
                return

            user.command_cache = command

            if user.command_cache:
                await output.print(f"recursively calling message_handler with cached command {user.command_cache}")
                await self.input_handler(user, "", output)
            else:
                await output_debug.print("successfully completed command sequence")
                user.command_cache_locked = False
                return
        #----------------------------------------------------------------------
        # case 5 is a temporary test case for the search function in search.py
        #----------------------------------------------------------------------
        elif Flag.CASE_5 in user.flag:
            user.flag.remove(Flag.CASE_5)
            possible_courses = self.course_search.search(msg.casefold())
            await output.print("courses: " + str(possible_courses))
            user.command_cache_locked = False
            return


    #--------------------------------------------------------------------------
    # HELPER FUNCTIONS FOR THE TEXT UI
    #--------------------------------------------------------------------------

    # Helper function that starts running the test_suite
    async def test(self, output:Output=Output(OUT.CONSOLE)):
        test_suite = Test1()
        output.flags.add(Flag.DEBUG)
        await test_suite.test(output)
        output.flags.remove(Flag.DEBUG)


    # returns whether multiple selections are present, meaning adding requires further input
    async def add_course(self, user:User, query:str, semester:int, output:Output=Output(OUT.CONSOLE)) -> bool:
        returned_courses = [self.catalog.get_course(c) for c in self.course_search.search(query)]

        if len(returned_courses) == 0:
            await output.print(f"Course {query} not found")
            return False
        elif len(returned_courses) > 1:
            await output.print(f"query {query} has multiple valid courses, please choose from list:")
            i = 1
            for c in returned_courses:
                output.print_hold(f"{i}: {repr(c)}")
                i += 1
            await output.print_cache()
            user.flag.add(Flag.SCHEDULE_COURSE_SELECT)
            user.schedule_course_search = returned_courses
            user.schedule_course_search_sem = semester
            return True

        course = returned_courses[0]
        user.get_current_schedule().add_course(course, semester)
        await output.print(f"Added course {course.name} to semester {semester}")
        return False


    # returns whether multiple selections are present, meaning removing requires further input
    async def remove_course(self, user:User, query:str, semester:int, output:Output=Output(OUT.CONSOLE)) -> bool:
        this_semester_courses = user.get_current_schedule().get_semester(semester)

        if len(this_semester_courses) == 0:
            await output.print(f"No courses in semester {semester}")
            return False
        semester_course_search = Search(this_semester_courses, True)
        returned_courses = [self.catalog.get_course(c) for c in semester_course_search.search(query)]

        if len(returned_courses) == 0:
            await output.print(f"Course {query} not found")
            return False
        elif len(returned_courses) > 1:
            await output.print(f"query {query} has multiple valid courses, please choose from list:")
            i = 1
            for c in returned_courses:
                output.print_hold(f"{i}: {repr(c)}")
                i += 1
            await output.print_cache()
            user.flag.add(Flag.SCHEDULE_COURSE_SELECT)
            user.schedule_course_search = returned_courses
            user.schedule_course_search_sem = semester
            return True

        course = returned_courses[0]
        user.get_current_schedule().remove_course(course, semester)
        await output.print(f"Removed course {course.name} from semester {semester}")
        return False

    
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

        template3 = Template("Data Structures", Course("Data Structures", "CSCI", 1200))

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
