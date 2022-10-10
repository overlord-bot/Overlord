from array import *
from discord.ext import commands
import discord
import asyncio
import json
import os
import sys

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .rules import Rules
from .schedule import Schedule
from .test_suite import Test1
from .user import User
from .user import Flag


#########################################################################
#                            IMPORTANT NOTE:                            #
#                                                                       #
# This class is created once and is not instigated for each user.       #
# It is essential to keep all user specific data, such as input flags   #
# (i.e. selection_flag) or message delivery methods (i.e. msg_hold)     #
# inside the User class, which is instigated for each user.             #
#########################################################################


class Degree_Planner(commands.Cog, name="Degree Planner"):

    # each user is assigned a User object and stored in this dictionary
    # Users = <username, User>
    users = dict()

    # a single copy of the catalog is kept in this class
    catalog = Catalog()

    def __init__(self, bot):
        self.bot = bot

    #-----------------------------------------------------------------------
    # Main message listener
    #
    # Generates a schedule for each user and then passes the message
    # content to a helper function which will read the message and
    # determine responses.
    #-----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):

        # ignore messages not from users
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            # self.users is a dictionary of existing users that link their name to a User object
            if message.author in self.users:
                await self.message_handler(message)
                print(f"returning user: {message.author}")
            else:
                user = User(message.author)
                self.users.update({message.author:user})
                await self.message_handler(message)
                print(f"new user: {message.author}")

        print("on message function ended")

    #-----------------------------------------------------------------------
    # This function is a temporary text based system to control the bot
    # it can all be replaced with different UI system later
    #-----------------------------------------------------------------------
    async def message_handler(self, message):
        user:User = self.users.get(message.author)

        if Flag.TEST_RUNNING in user.flag:
            await user.msg(message, "Test running, please hold on")
            return

        if message.content.casefold() == "!dp":
            user.flag.clear()
            
            await user.msg(message, f"Hiyaa, what would you like to do, {str(message.author)[0:str(message.author).find('#'):1]}?") # What would you like to do, <username without tag>?
            await user.msg(message, "input the number in chat:  1: begin test sequence 2: import courses from json file 9: run scheduler 0: cancel")

            # Sets the flag to true so the next input (except for "dp") is treated as a response to the selection
            user.flag.add(Flag.MENU_SELECT)
        
        elif Flag.MENU_SELECT in user.flag:
            user.flag.clear()

            # CASE 1: run test suite
            if message.content.casefold() == "1":
                print("INPUT 1 REGISTERED")
                user.flag.add(Flag.TEST_RUNNING)
                await self.test(message)
                await user.msg(message, "Test completed successfully, all assertions are met")
                user.flag.remove(Flag.TEST_RUNNING)

            # CASE 2: run data fetch from json
            elif message.content.casefold() == "2":
                print("INPUT 2 REGISTERED")
                # There are currently three acceptable places to store the course_data.json file, and this function
                # will check through them in the listed order:
                # 1) within a folder named "data" inside degree planner's directory
                # 2) degree planner's directory
                # 3) root directory of the project folder

                if os.path.isfile(os.getcwd() + "/cogs/degree planner/data/course_data.json"):
                    await user.msg(message, f"file found: {os.getcwd()}/cogs/degree planner/data/course_data.json")
                    f = open(os.getcwd() + "/cogs/degree planner/data/course_data.json")
                elif os.path.isfile(os.getcwd() + "/cogs/degree planner/course_data.json"):
                    await user.msg(message, f"file found: {os.getcwd()}/cogs/degree planner/course_data.json")
                    f = open(os.getcwd() + "/cogs/degree planner/course_data.json")
                elif os.path.isfile(os.getcwd() + "/course_data.json"):
                    await user.msg(message, f"file found: {os.getcwd()}/course_data.json")
                    f = open(os.getcwd() + "/course_data.json")

                else:
                    await user.msg(message, "file not found, terminating")
                    return
                json_data = json.load(f)
                f.close()
                await self.parse_courses(message, json_data)
                await user.msg(message, "Sucessfully parsed json data, printing catalog")
                await user.msg_hold(self.catalog.to_string())
                await user.msg_release(message, False)
                await user.msg(message, "parsing completed")

            # CASE 9: Begin actual scheduler
            elif message.content.casefold() == "9":
                user.flag.add(Flag.SCHEDULING)
                user.flag.add(Flag.SCHEDULE_SELECTION)
                await user.msg(message, "You are now in scheduling mode!")
                await user.msg(message, "Please enter the name of the schedule to modify. If the schedule entered does not exist, it will be created")

            # CASE 0: cancel selection operation
            elif message.content.casefold() == "0":
                await user.msg(message, "ok :(")

            # CASE 69: nice
            elif message.content.casefold() == "69":
                await user.msg(message, "nice")

            # else: display unknown response message
            else:
                await user.msg(message, "Unknown response, cancelling")

        elif Flag.SCHEDULING in user.flag:

            command_raw = message.content.split(",") # user input split up, will parse as a command
            command = [e.strip() for e in command_raw] # strips all strings
            command[:] = [e for e in command if e] # removes empty strings from list in place
            print("scheduling command: " + str(command))
            l = len(command)

            cmd = command[0].casefold()

            if not l:
                await user.msg(message, "no command detected")
                return

            if Flag.SCHEDULE_SELECTION in user.flag:
                schedule = user.get_schedule(cmd)
                if isinstance(schedule, str):
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
                    await user.msg(message, "not enough arguments")
                    return
                semester = int(command.pop(0))
                if semester not in range(0, sche.SEMESTERS_MAX):
                    await user.msg(message, "invalid semester, please enter number between 0 and 11")
                    return

                for course_name in command:
                    await user.msg(message, f"attempting to add course {course_name} to semester {semester}")
                    course = self.catalog.get_course(course_name)
                    if isinstance(course, str):
                        await user.msg(message, f"course {course_name} not found")
                        continue

                    sche.add_course(course, semester)
                    await user.msg(message, f"successfully added course {course_name} to semester {semester}")
                    
            elif cmd == "remove":
                command.pop(0)
                if l < 3:
                    await user.msg(message, "not enough arguments")
                    return
                semester = int(command.pop(0))
                if semester not in range(0, sche.SEMESTERS_MAX):
                    await user.msg(message, "invalid semester, please enter number between 0 and 11")
                    return

                for course_name in command:
                    course = self.catalog.get_course(course_name)
                    if isinstance(course, str) or course not in sche.get_semester(semester):
                        await user.msg(message, f"can't find course {course_name} in semester {semester}")
                        continue
                    sche.remove_course(course, semester)
                    await user.msg(message, f"successfully removed course {course_name} from semester {semester}")

            elif cmd == "print":
                await user.msg_hold(sche.to_string())
                await user.msg_release(message, False)

            #elif cmd == "fulfillment":

            elif cmd == "reschedule":
                await user.msg(message, "Understood, please enter schedule name to modify:")
                user.flag.add(Flag.SCHEDULE_SELECTION)

            elif cmd == "exit":
                await user.msg(message, "exiting scheduling mode")
                user.flag.remove(Flag.SCHEDULING)
                user.flag.remove(Flag.SCHEDULE_SELECTION)

            else:
                await user.msg(message, "unrecognized action")



    #-----------------------------------------------------------------------
    # Helper function that starts running the test_suite, can be replaced
    # by pytest later
    #-----------------------------------------------------------------------
    async def test(self, message):
        user = self.users.get(message.author)
        test_suite = Test1()
        user.flag.add(Flag.DEBUG)
        await test_suite.test(message, user)
        user.flag.remove(Flag.DEBUG)   

    #-----------------------------------------------------------------------
    # Loads json file data representing course data into course objects
    # and stores it into the catalog
    #-----------------------------------------------------------------------
    async def parse_courses(self, message, json_data):
        
        user = self.users.get(message.author)

        if Flag.TEST_RUNNING in user.flag:
            await user.msg(message, "Operation unavailable due to another user operation running")
            return

        await user.msg(message, "Beginning parsing json data into catalog")
        
        for element in json_data['courses']:

            # gets course name, major and course_id
            course = Course(element['name'], element['major'], int(element['id']))

            if 'credits' in element:
                course.credits = element['credits']
            
            if 'CI' in element:
                course.CI = element['CI']

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

            if 'prerequisites' in element:
                prereqs = element['prerequisites']
                if isinstance(prereqs, list):
                    for prereq in prereqs:
                        course.add_prerequisite(prereq.strip())
                elif prereqs != "":
                    course.add_prerequisite(prereqs.strip())

            if 'cross_listed' in element:
                cross_listed = element['cross_listed']
                if isinstance(cross_listed, list):
                    for cross in cross_listed:
                        course.add_cross_listed(cross.strip())
                elif cross_listed != "":
                    course.add_cross_listed(cross_listed.strip())

            if 'restricted' in element:
                course.restricted = element['restricted']

            if 'description' in element:
                course.description = element['description']

            self.catalog.add_course(course)
            await user.msg_hold(course.to_string())
        await user.msg_release(message, False)

async def setup(bot):
    await bot.add_cog(Degree_Planner(bot))
