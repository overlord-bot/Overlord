#basic calendar cog
#allows users to add/view/remove events from a calendar

from cogs.calendar.calendar_functions import CalHelper
import asyncio
from discord.ext import commands
import datetime

class Calendar(commands.Cog, name="Calendar"):
    def __init__(self, bot):
        self.bot = bot
        self.calhelper = CalHelper(bot)

    @commands.command(
        name="calendar",
        help="Add or view events on the calendar! Usage: !calendar <add/remove> <event> <date as in MM/DD/YYYY> or !calendar <clear> or !calendar <view> <week/month>"
    )
    async def calendar(self, context, action: str, *, event: str = None, date: str = None):
        """Adds or views events in the calendar. Usage: !calendar <add/remove> <event> <date as in MM/DD/YYYY> or !calendar <view/clear> <week/month>"""
        if action.lower() == "add":
            if event:
                await context.send(embed=self.calhelper.print_add_embed(event, date))
            else:
                await context.send("Please specify an event.")

        elif action.lower() == "view":
            if event:
                await context.send(embed=self.calhelper.print_calendar_embed(event.lower()))
            else:
                await context.send("Please specify a valid view.")

        elif action.lower() == "events":
            await context.send(embed=self.calhelper.check_next(event))

        elif action.lower() == "clear":
            await context.send(embed=self.calhelper.print_clear_embed())

        elif action.lower() == "remove":
            if event:
                await context.send(embed=self.calhelper.print_remove_embed(event))
            else:
                await context.send("Please specify an event.")
        else:
            await context.send("Please specify an action.")

    #used for the calendar timer function
    @commands.command(
        name="calendar_timer",
        help="Set a timer for date on the calendar! Usage: !calendar_timer <date as in MM/DD/YYYY>"
    )
    async def calendar_timer(self, context, date: str):
        """Sets a timer for the date on the calendar. Usage: !calendar_timer <date as in MM/DD/YYYY>"""
        timer = self.calhelper.set_timer(date)
        timer1 = str(datetime.timedelta(seconds=timer))
        await context.send("Timer set for " + str(timer1))
        await asyncio.sleep(timer)
        if date in self.dictionary:
            await context.send("It's " + date + "! " + " ".join(self.calhelper.dictionary[date]))

async def setup(bot):
    await bot.add_cog(Calendar(bot))