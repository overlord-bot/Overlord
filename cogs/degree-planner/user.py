from array import *
from enum import Enum
from discord.ext import commands
import discord
from .schedule import Schedule
from queue import Queue

class Flag(Enum):
    DEBUG = 0

    CMD_PAUSED = 100
    CMD_RUNNING = 101

class User():
    
    def __init__(self, id, output=None):
        self.id = id
        self.username = str(id)
        self.__schedules = dict() # all schedules this user created <schedule name, Schedule>
        self.curr_schedule = "" # empty string signifies no current schedule

        self.flag = set()

        self.command_queue = Queue()
        self.command_queue_locked = False
        self.command_decision = None
        self.command_paused = None

        self.output = output
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
