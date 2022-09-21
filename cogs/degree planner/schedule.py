from array import *
from discord.ext import commands
from course import *

class Schedule(commands.Cog, name="Degree Planner"):

    def __init__(self, bot):
        self.bot = bot

    master_list = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        elif message.content.startswith("create course"):
            await message.channel.send("generating a course")
            course = Course()
            course.name = "data structures"
            await message.channel.send("created " + course.name)


async def setup(bot):
    await bot.add_cog(Schedule(bot))