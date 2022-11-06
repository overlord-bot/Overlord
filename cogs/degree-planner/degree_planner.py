from array import *
from discord.ext import commands
import discord
import asyncio
import json
import os

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
from .command import *

#########################################################################
#                            IMPORTANT NOTE:                            #
#                                                                       #
# This class is created once and is not instigated for each user.       #
# It is essential to keep all user specific data inside the User class  #
#########################################################################

# just to help keep track of deployed versions without needing access to host
VERSION = "dev 10.1 (working fulfillment checker)"

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
    # returns whether or not the input was successfully processed
    # catch the return value to determine if a command needs to be re-entered
    #--------------------------------------------------------------------------
    async def message_handler(self, user:User, msg:str, output:Output=Output(OUT.CONSOLE)) -> bool:
        if Flag.CMD_PAUSED in user.flag:
            user.command_decision = msg.strip().casefold()
        else:
            if user.command_queue_locked:
                await output.print("queue busy, please try again later")
                return False
            user.command_queue_locked = True
            #await output.print("waiting for previous tasks to finish")
            user.command_queue.join()
            #await output.print("previous commands finshed, starting new ones!")
            commands = await self.parse_command(msg, output)
            for command in commands:
                user.command_queue.put(command)

        await self.command_handler(user, output)
        return True


    async def parse_command(self, cmd:str, output:Output=Output(OUT.CONSOLE)) -> list:
        arg_list = [e.strip().casefold() for e in cmd.split(",") if e.strip()]
        temp_queue = []
        last_command = None
        for e in arg_list:
            # if we find a command, push the last command to the queue and create new command
            if CMD.get(e) != CMD.NONE:
                if last_command != None:
                    temp_queue.append(last_command)
                last_command = Command(e)
            # otherwise, add this as an argument to the last command
            else:
                if last_command != None:
                    last_command.arguments.append(e)
                else:
                    await output.print("invalid command")
        # after exiting the loop, push the last command if it exists into the queue
        if last_command != None:
            temp_queue.append(last_command)
        return temp_queue


    # parser for input and executes commands
    async def command_handler(self, user:User, output:Output=Output(OUT.CONSOLE)):
        output_debug = Output(OUT.CONSOLE)

        # this while loop will keep running until all commands are executed with
        # one exception: if user input is requested to finish running a command
        #
        # if that is the case, this while loop will break (use break), 
        # the current command will be stored with the user, and user input 
        # will activate this loop again
        #
        # upon user input, the while loop will first execute the stored command,
        # and then continue running afterwards.
        #
        # NOTE: use break to stop this loop only when awaiting user input
        # and add Flag.CMD_PAUSED in user.flag, otherwise the loop can never
        # be entered again.
        #
        # NOTE: use continue if the current loop operation is done, this moves
        # the process to the next command
        while(not user.command_queue.empty() or Flag.CMD_PAUSED in user.flag):
            flag_done = True
            if Flag.CMD_PAUSED in user.flag:
                command:Command = user.command_paused
                flag_done = False
            else:
                command:Command = user.command_queue.get()

            if command.command == CMD.NONE:
                await output("there was an error executing your command")
                user.command_queue.task_done()
                continue

            if command.command == CMD.TEST:
                await output_debug.print("BEGINNING TEST")
                await output.print(f"Testing Degree Planner {VERSION}")
                await self.test(output_debug)
                await output_debug.print("FINISHED TEST")
                await output.print("Test completed successfully, all assertions met")
                if flag_done: 
                    user.command_queue.task_done()
                continue

            if command.command == CMD.IMPORT:
                await output_debug.print("BEGINNING DATA IMPORTING")
                await self.parse_data()
                await output_debug.print("FINISHED DATA IMPORTING")
                await output.print("parsing completed")
                if flag_done: 
                    user.command_queue.task_done()
                continue

            if command.command == CMD.FIND:
                if len(command.arguments) == 0:
                    await output.print("no arguments found, use find, [courses] to find matching courses")
                    if flag_done: 
                        user.command_queue.task_done()
                    continue
                for query in command.arguments:
                    possible_courses = self.course_search.search(query)
                    output.print_hold(f"courses matching {query}: ")
                    i = 1
                    for c in possible_courses:
                        course = self.catalog.get_course(c)
                        output.print_hold(f"  {i}: {course.major} {course.course_id} {course.display_name}")
                        i += 1
                    await output.print_cache()
                if flag_done: 
                    user.command_queue.task_done()
                continue

            if command.command == CMD.SCHEDULE:
                if not command.arguments:
                    await output.print("not enough arguments, please specify a schedule name")
                    if flag_done: 
                        user.command_queue.task_done()
                    continue
                schedule_name = command.arguments[0]
                schedule = user.get_schedule(schedule_name)
                if schedule == None:
                    await output.print(f"Schedule {schedule_name} not found, generating new one!")
                    user.new_schedule(schedule_name)
                    user.curr_schedule = schedule_name
                else:
                    await output.print(f"Successfully switched to schedule {schedule_name}!")
                    user.curr_schedule = schedule_name
                if flag_done: 
                    user.command_queue.task_done()
                continue

            schedule = user.get_current_schedule()
            if schedule == None:
                await output.print("no schedule selected")
                if flag_done: 
                    user.command_queue.task_done()
                continue

            if command.command == CMD.ADD or command.command == CMD.REMOVE:
                if Flag.CMD_PAUSED in user.flag:
                    decision = user.command_decision
                    courses = command.data_store
                    if not decision.isdigit() or int(decision) not in range(1, len(courses) + 1):
                        await output.print("Please enter a valid selection number")
                        break
                    course:Course = courses[int(decision) - 1]
                    command.arguments[1] = course.name
                    user.flag.remove(Flag.CMD_PAUSED)

                if not command.arguments[0].isdigit():
                    await output.print("semester must be a number")
                    if flag_done: 
                        user.command_queue.task_done()
                    continue
                semester = int(command.arguments[0])
                if semester not in range(0, schedule.SEMESTERS_MAX):
                    await output.print(f"Invalid semester {semester}, enter number between 0 and 11")
                    if flag_done: 
                        user.command_queue.task_done()
                    continue

                course = command.arguments[1]
                if command.command == CMD.ADD:
                    possible_courses = await self.add_course(user, course, semester, output)
                else:
                    possible_courses = await self.remove_course(user, course, semester, output)
                if possible_courses:
                    await output.print(f"query {course} has multiple valid courses, please choose from list:")
                    i = 1
                    for c in possible_courses:
                        output.print_hold(f"{i}: {repr(c)}")
                        i += 1
                    await output.print_cache()
                    command.data_store = possible_courses
                    user.command_paused = command
                    user.flag.add(Flag.CMD_PAUSED)
                    if flag_done: 
                        user.command_queue.task_done()
                    break

                if flag_done: 
                    user.command_queue.task_done()
                continue

            if command.command == CMD.PRINT:
                output.print_hold(str(schedule))
                await output.print_cache()
                if flag_done: 
                    user.command_queue.task_done()
                continue

            if command.command == CMD.DEGREE:
                if not command.arguments:
                    await output.print("no arguments found, use degree, <degree name> to set your schedule's degree")
                    if flag_done: 
                        user.command_queue.task_done()
                    continue
                else:
                    input = command.arguments[0]
                    degree = self.catalog.get_degree(input)
                    if degree == None:
                        await output.print(f"invalid degree entered: {input}")
                    else:
                        schedule.degree = degree
                        await output.print(f"set your degree to {degree.name}")
                if flag_done: 
                    user.command_queue.task_done()
                continue

            if command.command == CMD.FULFILLMENT:
                if schedule.degree == None:
                    await output.print("no degree specified")
                else:
                    output.print_hold(schedule.degree.fulfillment_msg(schedule.get_all_courses()))
                    await output.print_cache()

                if flag_done: 
                    user.command_queue.task_done()
                continue

        # we're done :D
        user.command_queue_locked = False

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
            return returned_courses
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
            return returned_courses
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

        await output.print(f"added degree {str(degree)} containing rule {str(rule)} to catalog")

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
