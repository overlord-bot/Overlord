#basic calendar cog
#allows users to add events to a calendar
#and view the calendar
#by using the command !calendar <add/view> <event>
#and !calendar <view>

import asyncio
import discord
from discord.ext import commands
import datetime
import os
import calendar
import datetime

class Calendar(commands.Cog, name="Calendar"):
        def __init__(self, bot):
            self.bot = bot
            self.calendar = []
            self.dictionary = {}
            self.calendar_file = "calendar.txt"
            self.load_calendar()
    
        #used to load the calendar from the calendar.txt file
        def load_calendar(self):
            if os.path.exists(self.calendar_file):
                with open(self.calendar_file, "r") as f:
                    for line in f:
                        self.calendar.append(line.strip())
            else:
                with open(self.calendar_file, "w") as f:
                    pass
    
        #used to add an event to the calendar
        def save_calendar(self):
            with open(self.calendar_file, "w") as f:
                for event in self.calendar:
                    f.write(event + "")

        #used to print remove embed
        def print_remove_embed(self):
            embed = discord.Embed(title="Calendar", description="Event removed!", color=0xff0000)
            return embed

        #used to print the clear embed    
        def print_clear_embed(self):
            embed = discord.Embed(title="Calendar", description="Calendar cleared!", color=0xff0000)
            return embed

        #used to print add embed
        def print_add_embed(self, event):
            date = event.split(" ")[-1]
            event = event.partition(date)[0]
            if date in self.dictionary:
                self.dictionary[date].append(event)
            else:
                self.dictionary[date] = [event]
            embed = discord.Embed(title="Calendar", description="Event added for " + date + "!", color=0xff0000)
            event = event + "\n"
            self.calendar.append(event)
            self.save_calendar()
            return embed

        #used to check to see if the day has an event
        def check_event(self, week_string, date):
            curr = ""
            if date < 10:  
                curr = "0" + str(date)
            else:
                curr = str(date)
            for key in self.dictionary.keys():
                if key[3:5] == curr:
                    for event in self.dictionary[key]:
                        week_string += "*"
            return week_string

        #used to print the calendar
        def print_calendar_embed(self):
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            currday = datetime.datetime.now().day

            embed = discord.Embed(title="Calendar", description="Calendar for " + calendar.month_name[month] + " " + str(year), color=0xff0000)
            cal = calendar.monthcalendar(year, month)
            week_string = ""
            for week in cal:
                week_string += "\n"
                for day in week:
                    if day == currday:
                        if day < 10:
                            week_string += "0"
                        week_string += str(day) + "<--"
                        week_string = self.check_event(week_string, day)
                        week_string += "\t"
                    elif day == 0:
                        week_string += " x\t\t"
                    elif len(str(day)) == 1:
                        week_string += "0" + str(day)
                        week_string = self.check_event(week_string, day)
                        week_string += "\t\t"
                    else:
                        week_string += str(day)
                        week_string = self.check_event(week_string, day)
                        week_string += "\t\t"
                embed.add_field(name=week_string, value="\u200b", inline=False)
                week_string = ""
            for date in sorted(self.dictionary):
                if int(date[:2]) == month:
                    embed.add_field(name=date, value="\n".join(self.dictionary[date]), inline=False)
            return embed

        #used to get the timer
        def set_timer(self, date):
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            day = now.day
            event_month = int(date[:2])
            event_day = int(date[3:5])
            event_year = int(date[6:])
            time_until_event0 = datetime.datetime(event_year, event_month, event_day) - datetime.datetime(year, month, day)
            time_until_event1 = time_until_event0.total_seconds()
            return time_until_event1

        @commands.command(
            name="calendar",
            help="Add or view events on the calendar! Usage: !calendar <add/remove> <event> <date as in MM/DD/YYYY> or !calendar <view/clear>"
        )
        async def calendar(self, context, action: str, *, event: str = None, date: str = None):
            """Adds or views events in the calendar."""
            if action.lower() == "add":
                if event:
                    await context.send(embed=self.print_add_embed(event))
                else:
                    await context.send("Please specify an event.")

            elif action.lower() == "view":
                await context.send(embed=self.print_calendar_embed())

            elif action.lower() == "clear":
                self.dictionary = {}
                self.calendar = []
                self.save_calendar()
                await context.send(embed=self.print_clear_embed())

            elif action.lower() == "remove":
                if event:
                    if event == "last":
                        self.calendar.pop()
                        self.save_calendar()
                        await context.send(embed=self.print_remove_embed())
                    elif event in self.calendar:
                        self.calendar.remove(event)
                        self.save_calendar()
                        await context.send(embed=self.print_remove_embed())
                    else:
                        await context.send("Event not found.")
                else:
                    await context.send("Please specify an event.")
            else:
                await context.send("Please specify an action.")

        @commands.command(
            name="calendar_timer",
            help="Set a timer for date on the calendar! Usage: !calendar_timer <date as in MM/DD/YYYY>"
        )
        async def calendar_timer(self, context, date: str):
            timer = self.set_timer(date)
            timer1 = str(datetime.timedelta(seconds=timer))
            await context.send("Timer set for " + str(timer1))
            await asyncio.sleep(timer)
            if date in self.dictionary:
                await context.send("It's " + date + "! " + " ".join(self.dictionary[date]))

async def setup(bot):
    await bot.add_cog(Calendar(bot))