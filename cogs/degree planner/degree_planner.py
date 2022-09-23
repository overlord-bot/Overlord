from array import *
from discord.ext import commands
import discord
import asyncio
import json

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .list_and_rules import List_and_rules
from .schedule import Schedule
from .test_suite import Test1


class Degree_Planner(commands.Cog, name="Degree Planner"):

    # each user is assigned a schedule object and stored in the dictionary below, with the format
    # Schedules = <author, Schedule>
    schedules = dict()

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

            #sets the flag to true so the next input (except for "dp") is treated as a response to the selection menu
            schedule.selection_flag = True
        
        elif schedule.selection_flag:
            schedule.selection_flag = False # resets selection flag
            if message.content.casefold() == "1":
                if schedule.test_running:
                    await schedule.msg(message, "Test is already running, please wait for its completion")
                else:
                    schedule.test_running = True
                    await self.test(message)

            elif message.content.casefold() == "2":
                await schedule.msg(message, "reading from data.json...")
                f = open("data.json")
                print("Successfully opened json file")
                json_data = json.load(f)
                print("Successfully loaded json file")
                await self.parse_courses(message, schedule, json_data)

            elif message.content.casefold() == "0":
                await schedule.msg(message, "ok :(")

            elif message.content.casefold() == "69":
                await schedule.msg(message, "nice")
            else:
                await schedule.msg(message, "Unknown response, cancelling")

    
    async def test(self, message):
        test_suite = Test1()
        await test_suite.test(message)

    async def parse_courses(self, message, schedule, json_data):
        for element in json_data['courses']:
            course = Course(element['name'], element['major'], int(element['id']))
            print(str(element) + " added successfully")

async def setup(bot):
    await bot.add_cog(Degree_Planner(bot))
