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
        #get path to calendar.json
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
        if user in self.events.keys():
            self.events[user]["calendar"] = self.events[user]["calendar"] + event + ""
            self.events[user]["events"].append(event)
        else:
            self.events[user] = {}
            self.events[user]["calendar"] = event + ""
            self.events[user]["events"] = [event]
        self.save_json()
        #print out the json file
        print(self.events)
        embed = discord.Embed(title="Calendar", description="Event added!", color=0xff0000)
        return embed
        