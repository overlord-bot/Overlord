from array import *
from discord.ext import commands
import discord

from ..utils.output import *
from .event import *
from .events.degree_planner_event import *
from .precondition import *
from .preconditions.degree_planner_listener import *
import threading
import asyncio

OUTERROR = Output(OUT.ERROR)
OUTWARNING = Output(OUT.WARN)
OUTINFO = Output(OUT.INFO)
OUTDEBUG = Output(OUT.DEBUG)
OUTCONSOLE = Output(OUT.CONSOLE)

class UniversalThread(threading.Thread):

    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.events = []
        self.preconditions = []
        self.keep_alive = True
        

    def run(self):
        print(f'{self.thread_name} {self.thread_ID} nya')
        self.runasync()

        #if self.keep_alive:
         #   timer = threading.Timer(1, self.run)
         #   timer.start()

    def runasync(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.run_events())
        loop.run_forever()

    async def run_events(self):
        for e in self.events:
            satisfied = await e.satisfied()
            if satisfied:
                e.run()

    def stop(self):
        self.keep_alive = False


class Slime(commands.Cog, name='Slime Lambda'):

    def __init__(self, bot):
        self.bot = bot
        self.running = True
        self.thread = None
        self.daemon_start()

    def _start_background_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def asyncio_run(coro, timeout):
        pass

    def daemon_start(self):
        self.thread = UniversalThread('daemon', '1')
        self.thread.keep_alive = True

        #adding dp listener
        self.thread.events.append(dp_event(self.bot))

        self.thread.start()

    def daemon_stop(self):
        self.thread.stop()

    @commands.command()
    async def startlambda(self, ctx):
        output = Output(OUT.DISCORD_CHANNEL, discord_channel=ctx.channel, output_type=OUTTYPE.EMBED)
        if self.running:
            await output.print('lambda already running')
            return
        else:
            await output.print('lambda starting')
            self.running = True
            self.daemon_start()

    @commands.command()
    async def stoplambda(self, ctx):
        output = Output(OUT.DISCORD_CHANNEL, discord_channel=ctx.channel, output_type=OUTTYPE.EMBED)
        if not self.running:
            await output.print('lambda already stopped')
            return
        else:
            await output.print('lambda stopping')
            self.running = False
            self.daemon_stop()


async def setup(bot):
    await bot.add_cog(Slime(bot))