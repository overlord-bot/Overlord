#helper file containing functions for the calendar json cog
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

    def check_user(self, user):
        if user not in self.events.keys():
            self.events = {user: {"events": {}, "calendar": ""}}
            self.save_json()
            return False
        return True

    def print_add_embed(self, event, user):
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
        #split event into date and event
        date = event.split(" ")[-1]
        event = event.replace(date, "")
        event = event[:-1]

        #if user is not in the json file, add them
        if self.check_user(user) == False:
            self.events[user]["events"][date].append(event)
        else:
            #if date is not in the json file, add it
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
        
    def check_event(self, week_string, date, user):
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

    def print_view_embed(self, user, username):
        self.check_user(user)
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
            week_string = "\n"
        embed.add_field(name=week_string, value="\u200b", inline=False)
        self.events[user]["calendar"] = week_string
        self.save_json()
        return embed