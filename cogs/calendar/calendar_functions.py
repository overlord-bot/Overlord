#helper file containing functions for the calendar cog
import discord
from discord.ext import commands
import datetime
import os
import calendar
import datetime

class CalHelper():
    def __init__(self, bot):
        self.bot = bot
        self.calendar = []
        self.events = {}
        self.load_calendar()

    #used to load the calendar from the calendar.txt file
    def load_calendar(self):
        if os.path.exists("calendar.txt"):
            with open("calendar.txt", "r") as f:
                for line in f:
                    self.calendar.append(line.strip())
        else:
            with open("calendar.txt", "w") as f:
                pass

    #used to add an event to the calendar
    def save_calendar(self):
        with open("calendar.txt", "w") as f:
            for event in self.calendar:
                f.write(event + "")

    #used to print remove embed
    def print_remove_embed(self, event):
        for key0 in self.events.values():
            print(key0)
        if event == "last":
            self.calendar.pop()
        elif event in self.events.keys():
            del self.events[event]
        #broken for now, will fix later
        elif event in self.events.values():
            for key in self.events.keys():
                if event in self.events[key]:
                    self.events[key].remove(event)
                    if len(self.events[key]) == 0:
                        del self.events[key]
        else:
            embed = discord.Embed(title="Calendar", description="Event not found!", color=0xff0000)
            return embed
        self.save_calendar()
        embed = discord.Embed(title="Calendar", description="Event removed!", color=0xff0000)
        return embed

    #used to print the clear embed    
    def print_clear_embed(self):
        self.events = {}
        self.calendar = []
        self.save_calendar()
        embed = discord.Embed(title="Calendar", description="Calendar cleared!", color=0xff0000)
        return embed

    #used to print add embed
    def print_add_embed(self, event):
        date = event.split(" ")[-1]
        event = event.partition(date)[0]
        if date in self.events:
            self.events[date].append(event)
        else:
            self.events[date] = [event]
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
        for key in self.events.keys():
            if key[3:5] == curr:
                for event in self.events[key]:
                    week_string += "*"
        return week_string

    #check if there is an event within the next num days
    def check_next(self, num):
        now = datetime.datetime.now()
        #convert now to int
        currday = int(now.strftime("%d"))
        embed = discord.Embed(title="Calendar", description="Events in the next " + str(num) + " days", color=0xff0000)
        for key in sorted(self.events.keys()):
            if int(key[3:5]) <= currday + int(num):
                embed.add_field(name=key, value="\n".join(self.events[key]), inline=False)
        return embed

    #used to print the calendar
    def print_calendar_embed(self, event):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        currday = datetime.datetime.now().day

        embed = discord.Embed(title="Calendar", description="Calendar for " + calendar.month_name[month] + " " + str(year), color=0xff0000)
        cal = calendar.monthcalendar(year, month)
        week_string = "Mon\t Tue\t Wed\t Thu\t Fri\t Sat\t Sun"
        #prints out the week calendar
        if event == "week":
            week_string += "\n"
            for week in cal:
                if currday in week:
                    for day in week:
                        if day == currday:
                            if day < 10:
                                week_string += "0"
                            week_string += str(day)
                            week_string = self.check_event(week_string, day)
                            week_string += "<-\t"
                        elif day == 0:
                            week_string += "  x\t\t"
                        elif len(str(day)) == 1:
                            week_string += "0" + str(day)
                            week_string = self.check_event(week_string, day)
                            week_string += "\t\t"
                        else:
                            week_string += str(day)
                            week_string = self.check_event(week_string, day)
                            week_string += "\t\t"
                    embed.add_field(name=week_string, value = "\u200b", inline=False)
        else:
            #prints out the month calendar
            for week in cal:
                week_string += "\n"
                for day in week:
                    if day == currday:
                        if day < 10:
                            week_string += "0"
                        week_string += str(day)
                        week_string = self.check_event(week_string, day)
                        week_string += "<-\t"
                    elif day == 0:
                        week_string += "  x\t\t"
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
        for date in sorted(self.events):
            if int(date[:2]) == month:
                embed.add_field(name=date, value="\n".join(self.events[date]), inline=False)
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
            