import discord
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="All commands", description="Type `!help [cog]` for more information on any of the following cogs")

        bot = self.context.bot.user
        embed.set_author(name=bot.name, icon_url=bot.avatar)

        for cog, commands in mapping.items():
            if cog is not None:
                command_names = [command.name for command in commands if command is not None]

                if command_names:
                    embed.add_field(name=cog.qualified_name, value=", ".join(command_names), inline=True)

        await self.get_destination().send(embed=embed)

def setup(bot):
  bot.help_command = HelpCommand()
