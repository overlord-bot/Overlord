from array import *
from discord.ext import commands
import discord
import asyncio
import json
import os

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .list_and_rules import List_and_rules
from .schedule import Schedule
from .test_suite import Test1
from .user import User


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
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            print("received input from user " + str(message.author))
            if message.author in self.users:
                await self.on_msg(message, self.users.get(message.author))
                print("returning user")
            else:
                user = User(message.author)
                self.users[message.author] = user
                await self.on_msg(message, self.users.get(message.author))
                print("new user")


    #-----------------------------------------------------------------------
    # This function is a temporary text based system to control the bot
    # it can all be replaced with different UI system later
    #-----------------------------------------------------------------------
    async def on_msg(self, message, user):
        if message.content.startswith("dp"):
            await user.msg(message, "hiyaa")
            await user.msg(message, "What would you like to do, " + str(message.author)[0:str(message.author).find('#'):1] + "?") # What would you like to do, <username without tag>?
            await user.msg(message, "input the number in chat:  1: begin test sequence 2: import from json file 0: cancel")

            # Sets the flag to true so the next input (except for "dp") is treated as a response to the selection
            user.selection_flag = True
        
        elif user.selection_flag:
            user.selection_flag = False

            # CASE 1: run test suite
            if message.content.casefold() == "1":
                print("INPUT 1 REGISTERED")
                if user.test_running:
                    await user.msg(message, "Operation is already running, please wait for its completion")
                else:
                    user.test_running = True
                    await self.test(message, user)
                    await user.msg(message, "Test completed")

            # CASE 2: run data fetch from json
            elif message.content.casefold() == "2":
                print("INPUT 2 REGISTERED")
                # There are currently three acceptable places to store the course_data.json file, and this function
                # will check through them in the listed order:
                # 1) within a folder named "data" inside degree planner's directory
                # 2) degree planner's directory
                # 3) root directory of the project folder

                if os.path.isfile(os.getcwd() + "/cogs/degree planner/data/course_data.json"):
                    await user.msg(message, "file found: " + os.getcwd() + "/cogs/degree planner/data/course_data.json")
                    f = open(os.getcwd() + "/cogs/degree planner/data/course_data.json")
                elif os.path.isfile(os.getcwd() + "/cogs/degree planner/course_data.json"):
                    await user.msg(message, "file found: " + os.getcwd() + "/cogs/degree planner/course_data.json")
                    f = open(os.getcwd() + "/cogs/degree planner/course_data.json")
                elif os.path.isfile(os.getcwd() + "/course_data.json"):
                    await user.msg(message, "file found: " + os.getcwd() + "/course_data.json")
                    f = open(os.getcwd() + "/course_data.json")

                else:
                    await user.msg(message, "file not found, terminating")
                    return
                json_data = json.load(f)
                await self.parse_courses(message, user, json_data)
                await user.msg(message, "Sucessfully parsed json data, printing catalog")
                await user.msg_hold(message, self.catalog.to_string())
                await user.msg_release(message, False)
                await user.msg(message, "Sucessfully printed catalog")

            # CASE 0: cancel selection operation
            elif message.content.casefold() == "0":
                await user.msg(message, "ok :(")

            # CASE 69: nice
            elif message.content.casefold() == "69":
                await user.msg(message, "nice")

            # else: display unknown response message
            else:
                await user.msg(message, "Unknown response, cancelling")


    #-----------------------------------------------------------------------
    # Helper function that starts running the test_suite, can be replaced
    # by pytest later
    #-----------------------------------------------------------------------
    async def test(self, message, user):
        test_suite = Test1()
        await test_suite.test(message, user)


    #-----------------------------------------------------------------------
    # Loads json file data representing course data into course objects
    # and stores it into the catalog
    #-----------------------------------------------------------------------
    async def parse_courses(self, message, user, json_data):
        if user.test_running:
            await user.msg(message, "Schedule unavailable due to another operation running")
            return
        await user.msg(message, "Beginning parsing json data into catalog")
        for element in json_data['courses']:
            course = Course(element['name'], element['major'], int(element['id']))
            self.catalog.add_course(course)
            await user.msg_hold(message, str(element))
        await user.msg_release(message, False)


async def setup(bot):
    await bot.add_cog(Degree_Planner(bot))
