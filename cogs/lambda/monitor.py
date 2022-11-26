from array import *
from discord.ext import commands
import discord

from ..utils.output import *

class Monitor():

    def check(self):
        raise NotImplementedError
