from array import *
from discord.ext import commands
import discord

from ..utils.output import *
from .event import *

class Precondition():

    def __init__(self, bot, name=''):
        self.bot = bot
        self.name = name

    async def satisfied(self):
        raise NotImplementedError

    def set(self, event:Event=None):
        raise NotImplementedError

    async def fetch(self):
        print('fetched precondition ' + self.name)
        return None