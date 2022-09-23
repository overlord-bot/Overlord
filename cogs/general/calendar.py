#basic calendar cog
#allows users to add events to a calendar
#and view the calendar
#by using the command !calendar <add/view> <event>
#and !calendar <view>

import discord
from discord.ext import commands
import datetime
import os
import calendar

class Calendar(commands.Cog, name="Calendar"):
        def __init__(self, bot):
            self.bot = bot
            self.calendar = []
            self.calendar_file = "calendar.txt"
            self.load_calendar()
    
        def load_calendar(self):
            if os.path.exists(self.calendar_file):
                with open(self.calendar_file, "r") as f:
                    for line in f:
                        self.calendar.append(line.strip())
            else:
                with open(self.calendar_file, "w") as f:
                    pass
    
        def save_calendar(self):
            with open(self.calendar_file, "w") as f:
                for event in self.calendar:
                    f.write(event + "")

        def print_remove_embed(self, event):
            embed = discord.Embed(title="Calendar", description="Event removed!", color=0xff0000)
            return embed

        def print_add_embed(self, event):
            event = event + "\n"
            self.calendar.append(event)
            self.save_calendar()
            embed = discord.Embed(title="Calendar", description="Event added!", color=0xff0000)
            embed.add_field(name=event, value="\u200b", inline=False)
            return embed

        def print_calendar_embed(self):
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            day = now.day

            embed = discord.Embed(title="Calendar", description="Calendar for " + calendar.month_name[month] + " " + str(year), color=0xff0000)
            cal = calendar.monthcalendar(year, month)

            for week in cal:
                week_string += "\n"
                for day in week:
                    if day == 0:
                        week_string += "-\t\t"
                    elif len(str(day)) == 1:
                        week_string += "0" + str(day) + "\t\t"
                    else:
                        week_string += str(day) + "\t\t"
                embed.add_field(name=week_string, value="\u200b", inline=False)
            return embed


        def print_clear_embed(self):
            embed = discord.Embed(title="Calendar", description="Calendar cleared!", color=0xff0000)
            return embed


        @commands.command(
            name="calendar",
            help="Add or view events on the calendar! Usage: !calendar <add/remove> <event> or !calendar <view/clear>"
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
                self.calendar = []
                self.save_calendar()
                await context.send(embed=self.print_clear_embed())

            elif action.lower() == "remove":
                if event:
                    if event == "last":
                        self.calendar.pop()
                        self.save_calendar()
                        await context.send(embed=self.print_remove_embed(event))
                    elif event in self.calendar:
                        self.calendar.remove(event)
                        self.save_calendar()
                        await context.send(embed=self.print_remove_embed(event))
                    else:
                        await context.send("Event not found.")
                else:
                    await context.send("Please specify an event.")
            else:
                await context.send("Please specify an action.")


async def setup(bot):
    await bot.add_cog(Calendar(bot))