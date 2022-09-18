#basic calendar cog
#allows users to add events to a calendar
#and view the calendar
#by using the command !calendar <add/view> <event>
#and !calendar <view>
#respectively
#the calendar is stored in a text file
#and is updated every time a new event is added
#or the calendar is viewed
#the calendar is also printed to the console
#when the bot is started

import discord
from discord.ext import commands
import datetime
import os

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

        def print_calendar(self):
            print("Calendar:")
            for event in self.calendar:
                print(event)
            print("")

        @commands.command()
        async def calendar(self, context, action: str, *, event: str = None):
            """Adds or views events in the calendar."""
            if action.lower() == "add":
                if event:
                    self.calendar.append(event)
                    self.save_calendar()
                    self.print_calendar()
                    await context.send("Event added to calendar.")
                else:
                    await context.send("Please specify an event.")
            elif action.lower() == "view":
                if self.calendar:
                    await context.send("Calendar:")
                    for event in self.calendar:
                        await context.send(event)
                else:
                    await context.send("Calendar is empty.")
            elif action.lower() == "clear":
                self.calendar = []
                self.save_calendar()
                self.print_calendar()
                await context.send("Calendar cleared.")
            elif action.lower() == "remove":
                if event:
                    if event in self.calendar:
                        self.calendar.remove(event)
                        self.save_calendar()
                        self.print_calendar()
                        await context.send("Event removed from calendar.")
                    else:
                        await context.send("Event not found.")
                else:
                    await context.send("Please specify an event.")
            else:
                await context.send("Please specify an action.")

async def setup(bot):
    await bot.add_cog(Calendar(bot))