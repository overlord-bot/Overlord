from array import *
from discord.ext import commands
import asyncio

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .list_and_rules import List_and_rules
from .schedule import Schedule


class Degree_Planner(commands.Cog, name="Degree Planner"):

    schedules = dict()

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            print("received input ")
            if message.author in self.schedules:
                await self.schedules.get(message.author).on_message(message)
                print("returning user")
            else:
                schedule = Schedule()
                self.schedules[message.author] = schedule
                await schedule.on_message(message)
                print("new user")



async def setup(bot):
    await bot.add_cog(Degree_Planner(bot))
