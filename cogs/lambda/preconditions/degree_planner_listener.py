from ..precondition import *

class dp_listener(Precondition):

    def __init__(self, bot, name='dp message listener'):
        super().__init__(bot, name)

    async def satisfied(self):
        print('yes')
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                print('yessss')
                async for message in channel.history(limit=2):
                    print(message)
                    if 'degree planner' in message.content.casefold():
                        print(str(message))
                        return True
        return False