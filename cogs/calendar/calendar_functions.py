#helper file containing functions for the calendar json cog
"""
format to add user data to json file:
{
    "user1": 
    [
        "events": 
        [
            "date": ["event1", "event2"],
            ...
        ],
    ],
    "user2":
    [
        "events":
        [
            "date": ["event1", "event2"],
            ...
        ],
    ],
    ...
}
"""
import discord
from discord.ext import commands
import os
import calendar
import datetime
import json
import asyncio

class CalHelperJson():
    def __init__(self, bot):
        self.bot = bot
        self.calendar = []
        self.events = {}
        self.path = os.path.join(os.path.dirname(__file__), "calendar.json")
        self.load_json()

    #if json file exists, load it
    def load_json(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.events = json.load(f)
        else:
            with open(self.path, "w") as f:
                pass

    #save the json file
    def save_json(self):
        with open(self.path, "w") as f:
            json.dump(self.events, f)

    #save the init data to the calendar_json in json format
    def save_calendar_json(self):
        with open(self.path, "w") as f:
            json.dump(self.calendar, f)

    #used for testing, clears the json file
    def print_clear_json(self):
        self.events = {}
        self.save_json()
        embed = discord.Embed(title="Calendar", description="Json file cleared!", color=0xff0000)
        return embed

    #checks to see if the user exists
    def check_user(self, user):
        if user not in self.events.keys():
            self.events = {
                user: 
                {
                    "events": {},
                }
            }
            self.save_json()
            self.CalHolidays(user)
            return False
        return True

    #checks to see if that day has an event
    def check_event(self, week_string, date, user, month):
        if self.check_user(user) == False:
            return week_string
        curr = ""
        if date < 10:  
            curr = "0" + str(date)
        else:
            curr = str(date)
        for key in self.events[user]["events"].keys():
            if key[3:5] == curr and key[0:2] == month:
                for event in self.events[user]["events"][key]:
                    week_string += "*"
        return week_string

    #adds holidays to calendar
    def CalHolidays(self, user):
        path = os.path.join(os.path.dirname(__file__), "holidays.txt")
        with open(path, "r") as f:
            for line in f:
                date = line.split(" ")[-1]
                line = line.replace(date, "")
                line = line[:-1]
                self.events[user]["events"][date] = [line]
        self.save_json()

    #adds the event to the json file
    def CalAdd(self, event, user):
        date = event.split(" ")[-1]
        if len(date) != 10 or date[2] != "/" or date[5] != "/" or int(date[0:2]) > 12 or int(date[3:5]) > 31 or int(date[6:10]) < 2022:
            embed = discord.Embed(title="Calendar", description="Invalid date format, please use MM/DD/YYYY", color=0xff0000)
            return embed
        event = event.replace(date, "")
        event = event[:-1]

        if self.check_user(user) == False:
            self.events[user]["events"][date] = [event]
        else:
            if date not in self.events[user]["events"].keys():
                self.events[user]["events"][date] = [event]
            elif date in self.events[user]["events"].keys():
                if event not in self.events[user]["events"][date]:
                    self.events[user]["events"][date].append(event)
                else:
                    embed = discord.Embed(title="Calendar", description="Event already exists!", color=0xff0000)
                    return embed
        self.save_json()
        embed = discord.Embed(title="Calendar", description="Event added!", color=0xff0000)
        return embed
        
    #constructs a visual of the calendar for the user
    def CalView(self, user, username):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        currday = datetime.datetime.now().day

        embed = discord.Embed(title="Calendar", description="Calendar for " + username, color=0xff0000)
        cal = calendar.monthcalendar(year, month)
        week_string = "Mon\t Tue\t Wed\t Thu\t Fri\t Sat\t Sun"
        for week in cal:
            week_string += "\n"
            for day in week:
                if day == currday:
                    if day < 10:
                        week_string += "0"
                    week_string += str(day)
                    week_string = self.check_event(week_string, day, user, str(month))
                    week_string += "<-\t"
                elif day == 0:
                    week_string += "  x\t\t"
                elif len(str(day)) == 1:
                    week_string += "0" + str(day)
                    week_string = self.check_event(week_string, day, user, str(month))
                    week_string += "\t\t"
                else:
                    week_string += str(day)
                    week_string = self.check_event(week_string, day, user, str(month))
                    week_string += "\t\t"
            week_string += "\n"
        embed.add_field(name=week_string, value="\u200b", inline=False)
        for key in sorted(self.events[user]["events"].keys()):
            if key[0:2] == str(month):
                embed.add_field(name=key, value="\n".join(self.events[user]["events"][key]), inline=False)
        self.save_json()
        return embed

    #removes an event from the json file
    def CalRemove(self, event, user):
        date = event.split(" ")[-1]
        if self.check_user(user) == False:
            embed = discord.Embed(title="Calendar", description="No events to remove!", color=0xff0000)
            return embed
        else:
            if event == date and date in self.events[user]["events"].keys():
                del self.events[user]["events"][date]
                self.save_json()
                embed = discord.Embed(title="Calendar", description="Event removed!", color=0xff0000)
                return embed
            else:
                for key in self.events[user]["events"].keys():
                    if event in self.events[user]["events"][key]:
                        self.events[user]["events"][key].remove(event)
                        if len(self.events[user]["events"][key]) == 0:
                            del self.events[user]["events"][key]
                        self.save_json()
                        embed = discord.Embed(title="Calendar", description="Event removed!", color=0xff0000)
                        return embed
        embed = discord.Embed(title="Calendar", description="Event not found!", color=0xff0000)
        return embed

    #edit an event
    def CalEditEvent(self, event, user):
        old_event = str(event.split("/")[1])
        old_event = old_event[:-1]
        new_event = str(event.split("/")[2])
        if self.check_user(user) == False:
            embed = discord.Embed(title="Calendar", description="No events to edit!", color=0xff0000)
            return embed
        for key in self.events[user]["events"].keys():
            if old_event in self.events[user]["events"][key]:
                self.events[user]["events"][key].remove(old_event)
                self.events[user]["events"][key].append(new_event)
                self.save_json()
                embed = discord.Embed(title="Calendar", description="Event edited!", color=0xff0000)
                return embed
        embed = discord.Embed(title="Calendar", description="Event not found!", color=0xff0000)
        return embed
            
    #edit a date by changing the events in that date to another date
    def CalEditDate(self, event, user):
        first = event.split(" ")[0]
        last = event.split(" ")[-1]
        if self.check_user(user) == False:
            embed = discord.Embed(title="Calendar", description="No events to edit!", color=0xff0000)
            return embed
        if first not in self.events[user]["events"].keys():
            embed = discord.Embed(title="Calendar", description="Event does not exist!", color=0xff0000)
            return embed
        else:
            self.events[user]["events"][last] = self.events[user]["events"][first]
            del self.events[user]["events"][first]
            self.save_json()
            embed = discord.Embed(title="Calendar", description="Event edited!", color=0xff0000)
            return embed

    #get all events for a specific date in a string
    def CalGetDate(self, date, user):
        if self.check_user(user) == False:
            embed = "New User: no events added yet!"
            return embed
        if date not in self.events[user]["events"].keys():
            embed = "No events for this date!"
            return embed
        else:
            embed = "\nReminder for " + date + ":\n"
            for event in self.events[user]["events"][date]:
                embed += event + "\n"
            return embed
