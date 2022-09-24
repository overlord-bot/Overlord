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


#########################################################################
#                            IMPORTANT NOTE:                            #
#                                                                       #
# This class is created once and is NOT instigated for each user.       #
# It is essential to keep all user specific data, such as input flags   #
# (i.e. selection_flag) or message delivery methods (i.e. msg_hold)     #
# inside the schedule class, which IS instigated for each user.         #
#########################################################################


class Degree_Planner(commands.Cog, name="Degree Planner"):

    # each user is assigned a schedule object and stored in the dictionary below, with the format
    # Schedules = <author, Schedule>
    schedules = dict()
    catalog = Catalog()

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            print("received input from user " + str(message.author))
            if message.author in self.schedules:
                await self.on_msg(message, self.schedules.get(message.author))
                print("returning user")
            else:
                schedule = Schedule()
                self.schedules[message.author] = schedule
                await self.on_msg(message, self.schedules.get(message.author))
                print("new user")

    #-----------------------------------------------------------------------
    # This function is a temporary text based system to control the bot
    # it can all be replaced with different UI system later
    #-----------------------------------------------------------------------
    async def on_msg(self, message, schedule):
        if message.content.startswith("dp"):
            await schedule.msg(message, "hiyaa")
            await schedule.msg(message, "What would you like to do, " + str(message.author)[0:str(message.author).find('#'):1] + "?")
            await schedule.msg(message, "input the number in chat:  1: begin test sequence 2: import from json file 0: cancel")

            # Sets the flag to true so the next input (except for "dp") is treated as a response to the selection menu
            schedule.selection_flag = True
        
        elif schedule.selection_flag:
            schedule.selection_flag = False

            # CASE 1: run test suite
            if message.content.casefold() == "1":
                print("INPUT 1 REGISTERED")
                if schedule.test_running:
                    await schedule.msg(message, "Operation is already running, please wait for its completion")
                else:
                    schedule.test_running = True
                    await self.test(message, schedule)
                    await schedule.msg(message, "Test completed")

            # CASE 2: run data fetch from json
            elif message.content.casefold() == "2":
                print("INPUT 2 REGISTERED")
                # There are currently three acceptable places to store the course_data.json file, and this function
                # will check through them in the listed order:
                # 1) within a folder named "data" inside degree planner's directory
                # 2) degree planner's directory
                # 3) root directory of the project folder

                if os.path.isfile(os.getcwd() + "\\cogs\\degree planner\\data\\course_data.json"):
                    await schedule.msg(message, "file found: " + os.getcwd() + "\\cogs\\degree planner\\data\\course_data.json")
                    f = open(os.getcwd() + "\\cogs\\degree planner\\data\\course_data.json")
                elif os.path.isfile(os.getcwd() + "\\cogs\\degree planner\\course_data.json"):
                    await schedule.msg(message, "file found: " + os.getcwd() + "\\cogs\\degree planner\\course_data.json")
                    f = open(os.getcwd() + "\\cogs\\degree planner\\course_data.json")
                elif os.path.isfile(os.getcwd() + "\\course_data.json"):
                    await schedule.msg(message, "file found: " + os.getcwd() + "\\course_data.json")
                    f = open(os.getcwd() + "\\course_data.json")

                else:
                    await schedule.msg(message, "file not found, terminating")
                    return
                json_data = json.load(f)
                await self.parse_courses(message, schedule, json_data)
                await schedule.msg(message, "Sucessfully parsed json data, printing catalog")
                await schedule.msg_hold(message, self.catalog.to_string())
                await schedule.msg_release(message, False)
                await schedule.msg(message, "Sucessfully printed catalog")

            # CASE 0: cancel selection operation
            elif message.content.casefold() == "0":
                await schedule.msg(message, "ok :(")

            # CASE 69: nice
            elif message.content.casefold() == "69":
                await schedule.msg(message, "nice")

            # else: display unknown response message
            else:
                await schedule.msg(message, "Unknown response, cancelling")

    
    async def test(self, message, schedule):
        test_suite = Test1()
        await test_suite.test(message, schedule)

    async def parse_courses(self, message, schedule, json_data):
        if schedule.test_running:
            await schedule.msg(message, "Schedule unavailable due to another operation running")
            return
        await schedule.msg(message, "Beginning parsing json data into catalog")
        for element in json_data['courses']:
            course = Course(element['name'], element['major'], int(element['id']))
            self.catalog.add_course(course)
            await schedule.msg_hold(message, str(element))
        await schedule.msg_release(message, False)

async def setup(bot):
    await bot.add_cog(Degree_Planner(bot))
