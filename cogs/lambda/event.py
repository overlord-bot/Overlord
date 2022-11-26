from array import *
from discord.ext import commands
import discord

from ..utils.output import *


class Event():
    def __init__(self, bot, preconditions:set=None):
        self.bot = bot
        self.preconditions = set() if preconditions == None else preconditions

    def run(self):
        raise NotImplementedError

    async def satisfied(self) -> bool:
        for p in self.preconditions:
            satisfied = await p.satisfied()
            if not satisfied: 
                return False
        return True