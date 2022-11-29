from array import *
from enum import Enum
from discord.ext import commands
import discord
from .schedule import Schedule
from queue import Queue
import json

class Flag(Enum):
    CMD_PAUSED = 100
    CMD_RUNNING = 101


class User():
    
    def __init__(self, id):
        self.id = id # unique id for user
        self.username = str(id) # username to display
        self.discord_user = None # discord user object, if applicable
        self.__schedules = dict() # all schedules this user created <schedule name, Schedule>
        self.curr_schedule = "" # schedule to modify

        self.flag = set()

        self.command_queue = Queue()
        self.command_queue_locked = False
        self.command_decision = None
        self.command_paused = None

        self.admin = False # admin for the bot


    def get_all_schedules(self) -> Schedule:
        return self.__schedules.values()


    def get_schedule(self, schedule_name:str) -> Schedule:
        if schedule_name not in self.__schedules:
            return None
        return self.__schedules.get(schedule_name)


    def new_schedule(self, schedule_name:str):
        schedule = Schedule(schedule_name)
        self.__schedules.update({schedule_name : schedule})


    def add_schedule(self, schedule_name:str, schedule:Schedule):
        self.__schedules.update({schedule_name : schedule})


    def get_current_schedule(self):
        return self.get_schedule(self.curr_schedule)


    def rename_schedule(self, old_name:str, new_name:str) -> bool:
        if old_name not in self.__schedules or new_name in self.__schedules:
            return False
        else:
            self.__schedules.update({new_name : self.__schedules.get(old_name)})
            self.__schedules.pop(old_name)
            return True

    def json(self):
        user = dict()
        user.update({'username':self.username})
        user.update({'id':self.id})
        user.update({'discord user':True if self.discord_user != None else False})
        schedules = list()
        for s in self.__schedules.keys():
            schedules.append(s)
        user.update({'schedules':schedules})
        user.update({'admin':self.admin})
        user.update({'commands in queue':self.command_queue.qsize()})
        return json.dumps(user)

    def __repr__(self):
        schedule_names = ""
        for s in self.__schedules.keys():
            schedule_names += f"[ {s} ] "
        return f"{str(self.username)}'s schedules: {schedule_names}"


    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self.username == other.username:
            return True
        return False


    def __hash__(self):
        return hash(self.id)
