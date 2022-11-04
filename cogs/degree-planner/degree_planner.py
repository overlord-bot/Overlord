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
        # Users = <username, User>
        self.users = dict()
        self.catalog = Catalog()
        self.search = Search(self.catalog.get_all_courses())
        self.debug_id = 0

        # just to help keep track of deployed versions through discord commands
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
            self.debug_id+=1
            if message.author in self.users:
                print(f"received msg from returning user: {message.author}; msg id: {self.debug_id}")
                await self.message_handler(message)
            else:
                print(f"received msg from new user: {message.author}; msg id: {self.debug_id}")
                user = User(message.author)
                self.users.update({message.author:user})
                await self.message_handler(message)

        print(f"end of message handler function; msg id: {self.debug_id}")


    #--------------------------------------------------------------------------
    # This function is a temporary text based system to control the bot
    # it can all be replaced with different UI system later
    #--------------------------------------------------------------------------
    async def message_handler(self, message):
        user:User = self.users.get(message.author)
        msg = message.content

        if Flag.TEST_RUNNING in user.flag:
            await user.msg(message, "Test running, please try again later")
            return

        # if we receive a command in the format !dp <int>
        if (msg.casefold().startswith("!dp") and len(msg.split(' ')) == 2 and 
            msg.split(' ')[1].isdigit()):
            print("detected compound dp command")
            # simulates as if the user typed in !dp and <int> separately
            user.flag.add(Flag.MENU_SELECT)
            # changes msg to be the !dp number
            msg = msg.split(' ')[1]

        # main menu command
        if msg.casefold() == "!dp":
            user.flag.clear()
            # prints "what would you like to do, <username without tag>?"
            await user.msg(message, f"Hiyaa, what would you like to do, " + \
                f"{str(message.author)[0:str(message.author).find('#'):1]}?") 
            await user.msg(message, 
                "Please input a number in chat:  " + \
                "1: begin test sequence " + \
                "2: import courses from json file " + \
                "9: run scheduler " + \
                "0: cancel")
            await user.msg(message, f"Degree Planner version: {self.VERSION}")

            user.flag.add(Flag.MENU_SELECT)
        
        #----------------------------------------------------------------------
        # main menu command !dp argument cases:
        #----------------------------------------------------------------------
        elif Flag.MENU_SELECT in user.flag:
            user.flag.clear()

            # CASE 1: run test suite
            if msg.casefold() == "1":
                print("INPUT 1 REGISTERED")
                user.flag.add(Flag.TEST_RUNNING)
                print("BEGINNING TEST")
                await self.test(message)
                print("FINISHED TEST")
                await user.msg(message, 
                    "Test completed successfully, all assertions met")
                user.flag.remove(Flag.TEST_RUNNING)

            # CASE 2: run data fetch from json
            # this will load both courses and degrees
            elif msg.casefold() == "2":
                print("INPUT 2 REGISTERED")

                # redirects user messages into terminal, too much data for discord chat
                user.flag.add(Flag.DEBUG)

                catalog_file = "catalog_results.json"
                degree_file = "class_results.json"

                await self.parse_courses(message, catalog_file)
                await user.msg(message, "Sucessfully parsed catalog data")
                
                self.search.generate_index()

                await self.parse_degrees(message, degree_file)
                await user.msg(message, "Sucessfully parsed degree data, printing catalog")
                await user.msg_hold(str(self.catalog))
                await user.msg_release(message, False)

                await user.force_msg(message, "parsing completed")

            #CASE 5: Search course (TEMPORARY TESTING PURPOSES)
            elif msg.casefold() == "5":
                print("INPUT 5 REGISTERED")
                await user.msg(message, "Enter the course")
                user.flag.add(Flag.CASE_5)

            # CASE 9: Begin actual scheduler, the main feature of this program
            elif msg.casefold() == "9":
                print("INPUT 9 REGISTERED")
                user.flag.add(Flag.SCHEDULING)
                user.flag.add(Flag.SCHEDULE_SELECTION)
                await user.msg(message, "You are now in scheduling mode!")
                await user.msg(message, "Enter the name of the schedule to modify. " + \
                    "If the schedule entered doesn't exist, it will be created")

            # CASE 0: cancel selection operation
            elif msg.casefold() == "0":
                await user.msg(message, "ok :(")

            # CASE 69: nice
            elif msg.casefold() == "69":
                await user.msg(message, "nice")

            else:
                await user.msg(message, "Unknown response, cancelling")

        #----------------------------------------------------------------------
        # course scheduling mode, the feature intended to be used in the end
        #----------------------------------------------------------------------
        elif Flag.SCHEDULING in user.flag:

            command_raw = msg.split(",") # user input split up, will parse as a command
            command = [e.strip().casefold() for e in command_raw] # strips and lowercases all args
            command = [e for e in command if e] # removes empty strings from list
            print("Inputted scheduling command: " + str(command))
            cmd = command[0] # command str will be modified later, this assignment is necessary!
            l = len(command) # command str will be modified later, this assignment is necessary!

            if not l:
                await user.msg(message, "no command detected")
                return

            if Flag.SCHEDULE_SELECTION in user.flag:
                schedule = user.get_schedule(cmd)
                if schedule == None:
                    await user.msg(message, f"Schedule {cmd} not found, generating new one!")
                    user.new_schedule(cmd)
                    user.curr_schedule = cmd
                else:
                    await user.msg(message, f"Successfully switched to schedule {cmd}!")
                    user.curr_schedule = cmd
                user.flag.remove(Flag.SCHEDULE_SELECTION)
                return

            sche = user.get_schedule(user.curr_schedule)

            if cmd == "add":
                command.pop(0)
                if l < 3:
                    await user.msg(message, "Not enough arguments")
                    return
                semester = int(command.pop(0))
                if semester not in range(0, sche.SEMESTERS_MAX):
                    await user.msg(message, "Invalid semester, enter number between 0 and 11")
                    return

                for course_name in command:
                    course = self.catalog.get_course(course_name)
                    if course == None:
                        await user.msg(message, f"Course {course_name} not found")
                        continue

                    sche.add_course(course, semester)
                    await user.msg(message, f"Added course {course_name} to semester {semester}")
                    
            elif cmd == "remove":
                command.pop(0)
                if l < 3:
                    await user.msg(message, "Not enough arguments")
                    return
                semester = int(command.pop(0))
                if semester not in range(0, sche.SEMESTERS_MAX):
                    await user.msg(message, "Invalid semester, enter number between 0 and 11")
                    return

                for course_name in command:
                    course = self.catalog.get_course(course_name)
                    if course == None or course not in sche.get_semester(semester):
                        await user.msg(message, f"Can't find course {course_name} in semester {semester}")
                        continue
                    sche.remove_course(course, semester)
                    await user.msg(message, f"Removed course {course_name} from semester {semester}")

            elif cmd == "print":
                await user.msg_hold(str(sche))
                await user.msg_release(message, False)

            elif cmd == "degree":
                command.pop(0)
                if l != 2:
                    await user.msg(message, "incorrect amount of arguments, " + \
                        "use degree,<degree name> to set your schedule's degree")
                else:
                    user.get_current_schedule().degree = self.catalog.get_degree(command.pop(0))
                    await user.msg(message, f"set degree to {user.get_current_schedule().degree.name}")


            elif cmd == "fulfillment":
                if user.get_current_schedule().degree == None:
                    await user.msg(message, "no degree specified")
                else:
                    await user.msg_hold(user.get_current_schedule().
                        degree.fulfillment_msg(user.get_current_schedule().get_all_courses()))
                    await user.msg_release(message, False)

            elif cmd == "reschedule":
                await user.msg(message, "Understood, please enter schedule name to modify:")
                user.flag.add(Flag.SCHEDULE_SELECTION)

            elif cmd == "exit":
                await user.msg(message, "Exiting scheduling mode")
                user.flag.remove(Flag.SCHEDULING)

            else:
                await user.msg(message, "Unrecognized action")

        #----------------------------------------------------------------------
        # case 5 is a temporary test case for the search function in search.py
        #----------------------------------------------------------------------
        elif Flag.CASE_5 in user.flag:
            user.flag.remove(Flag.CASE_5)
            possible_courses = self.search.search(message.content.casefold())
            await user.msg(message, "possible courses: " + str(possible_courses))


    #--------------------------------------------------------------------------
    # Helper function that starts running the test_suite, can be replaced
    # by pytest later
    #--------------------------------------------------------------------------
    async def test(self, message):
        user = self.users.get(message.author)
        test_suite = Test1()
        user.flag.add(Flag.DEBUG)
        await test_suite.test(message, user)
        user.flag.remove(Flag.DEBUG)   


    #--------------------------------------------------------------------------
    # parses json data of format [{course attribute : value}] 
    # into a set of Course objects stored in Catalog
    #--------------------------------------------------------------------------
    async def parse_courses(self, message, file_name):
        
        user = self.users.get(message.author)

        # will not parse if the test is running to prevent data loss since Catalog is shared
        # note that running a test will destroy all data within the Catalog, 
        # so rerunning this method is necessary after a test
        if Flag.TEST_RUNNING in user.flag:
            await user.msg(message, "Operation unavailable due to another user operation running")
            return
        await user.msg(message, "Beginning parsing course data into catalog")

        # There are 4 locations for catalog_results and class_results, checked in this order:
        # 1) /cogs/webcrawling/
        # 2) /cogs/degree-planner/data/
        # 3) /cogs/degree-planner/
        # 4) / (root directory of bot)
        if os.path.isfile(os.getcwd() + "/cogs/webcrawling/" + file_name):
            await user.msg(message, f"file found: {os.getcwd()}/cogs/webcrawling/" + file_name)
            file_catalog_results = open(os.getcwd() + "/cogs/webcrawling/" + file_name)
        elif os.path.isfile(os.getcwd() + "/cogs/degree-planner/data/" + file_name):
            await user.msg(message, f"file found: {os.getcwd()}/cogs/degree-planner/data/" + file_name)
            file_catalog_results = open(os.getcwd() + "/cogs/degree-planner/data/" + file_name)
        elif os.path.isfile(os.getcwd() + "/cogs/degree-planner/" + file_name):
            await user.msg(message, f"file found: {os.getcwd()}/cogs/degree-planner/" + file_name)
            file_catalog_results = open(os.getcwd() + "/cogs/degree-planner/" + file_name)
        elif os.path.isfile(os.getcwd() + "/" + file_name):
            await user.msg(message, f"file found: {os.getcwd()}/" + file_name)
            file_catalog_results = open(os.getcwd() + "/" + file_name)
        else:
            await user.msg(message, "catalog file not found")
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
    async def parse_degrees(self, message, file_name):
        
        user = self.users.get(message.author)

        # will not parse if the test is running to prevent data loss since Catalog is shared
        # note that running a test will destroy all data within the Catalog, 
        # so rerunning this method is necessary after a test
        if Flag.TEST_RUNNING in user.flag:
            await user.msg(message, "Operation unavailable due to another user operation running")
            return
        await user.msg(message, "Beginning parsing degree data into catalog")

        if os.path.isfile(os.getcwd() + "/cogs/webcrawling/" + file_name):
            await user.msg(message, f"file found: {os.getcwd()}/cogs/webcrawling/" + file_name)
            file_degree_results = open(os.getcwd() + "/cogs/webcrawling/" + file_name)
        elif os.path.isfile(os.getcwd() + "/cogs/degree-planner/data/" + file_name):
            await user.msg(message, f"file found: {os.getcwd()}/cogs/degree-planner/data/" + file_name)
            file_degree_results = open(os.getcwd() + "/cogs/degree-planner/data/" + file_name)
        elif os.path.isfile(os.getcwd() + "/cogs/degree-planner/" + file_name):
            await user.msg(message, f"file found: {os.getcwd()}/cogs/degree-planner/" + file_name)
            file_degree_results = open(os.getcwd() + "/cogs/degree-planner/" + file_name)
        elif os.path.isfile(os.getcwd() + "/" + file_name):
            await user.msg(message, f"file found: {os.getcwd()}/" + file_name)
            file_degree_results = open(os.getcwd() + "/" + file_name)
        else:
            await user.msg(message, "degree file not found")
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

        print(f"added degree {str(degree)} containing rule {str(rule)} to catalog")

        '''
        #----------------------------------------------------------------------
        # Begin iterating through json_data
        #
        # json data format: dictionary of degrees : list of dictionaries each representing a course
        # <degree name : [<course attribute : value>]
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
