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
        "calendar": string,
    ],
    "user2":
    [
        "events":
        [
            "date": ["event1", "event2"],
            ...
        ],
        "calendar": string,
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
        embed = discord.Embed(title="Calendar", description="Calendar cleared!", color=0xff0000)
        return embed

    #checks to see if the user exists
    def check_user(self, user):
        if user not in self.events.keys():
            self.events = {user: {"events": {}, "calendar": ""}}
            self.save_json()
            return False
        return True

    #adds the event to the json file
    def print_add_embed(self, event, user):
        date = event.split(" ")[-1]
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
        
    #checks to see if that day has an event
    def check_event(self, week_string, date, user):
        if self.check_user(user) == False:
            return week_string
        curr = ""
        if date < 10:  
            curr = "0" + str(date)
        else:
            curr = str(date)
        for key in self.events[user]["events"].keys():
            if curr == key[3:5]:
                for event in self.events[user]["events"][key]:
                    week_string += "*"
        return week_string

    #constructs a visual of the calendar for the user
    def print_view_embed(self, user, username):
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
                    week_string = self.check_event(week_string, day, user)
                    week_string += "<-\t"
                elif day == 0:
                    week_string += "  x\t\t"
                elif len(str(day)) == 1:
                    week_string += "0" + str(day)
                    week_string = self.check_event(week_string, day, user)
                    week_string += "\t\t"
                else:
                    week_string += str(day)
                    week_string = self.check_event(week_string, day, user)
                    week_string += "\t\t"
            week_string += "\n"
        embed.add_field(name=week_string, value="\u200b", inline=False)
        for key in sorted(self.events[user]["events"].keys()):
            if key[0:2] == str(month):
                embed.add_field(name=key, value="\n".join(self.events[user]["events"][key]), inline=False)
        self.events[user]["calendar"] = week_string
        self.save_json()
        return embed

    #removes an event from the json file
    def print_remove_embed(self, event, user):
        if self.check_user(user) == False:
            embed = discord.Embed(title="Calendar", description="No events to remove!", color=0xff0000)
            return embed
        if event not in self.events[user]["events"].keys():
            embed = discord.Embed(title="Calendar", description="Event does not exist!", color=0xff0000)
            return embed
        else:
            del self.events[user]["events"][event]
            self.save_json()
            embed = discord.Embed(title="Calendar", description="Event removed!", color=0xff0000)
            return embed
