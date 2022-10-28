#basic calendar json cog
#allows users to add/view/remove events from a calendar

from cogs.calendar.calendar_functionsjson import CalHelperJson
from discord.ext import commands

class CalendarJson(commands.Cog, name="CalendarJson"):
    def __init__(self, bot):
        self.bot = bot
        self.calhelper = CalHelperJson(bot)

    @commands.command(
        name="calendarv2",
        help="Add or view events on the calendar! Usage: !calendarjson <add/remove> <event> <date as in MM/DD/YYYY> or !calendar <clear> or !calendar <view> <week/month>"
    )
    async def calendar(self, context, action: str, *, event: str = None, date: str = None):
        """Adds or views events in the calendar. Usage: !calendar <add/remove> <event> <date as in MM/DD/YYYY> or !calendar <view/clear> <week/month>"""
        #get the discord user id who sent the message
        user_id = context.message.author.id
        user_name = context.message.author.name
        if action.lower() == "add":
            if event:
                await context.send(embed=self.calhelper.print_add_embed(event, user_id))
            else:
                await context.send("Please specify an event.")
        elif action.lower() == "clear":
            await context.send(embed=self.calhelper.print_clear_json())
        elif action.lower() == "view":
            await context.send(embed=self.calhelper.print_view_embed(user_id, user_name))
        else:
            await context.send("Please specify an action.")

async def setup(bot):
    await bot.add_cog(CalendarJson(bot))
    