from ..event import *
from ..preconditions.degree_planner_listener import *

class dp_event(Event):

    def __init__(self, bot, preconditions:set=None):
        super().__init__(bot, {dp_listener(bot)})
        print('dp_event initialized')
        

    def run(self):
        print('degree planner just fucking printed to console lmao')