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

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"Help for {cog.qualified_name}")

        embed.description = "\n".join(f"**{command.qualified_name} {command.signature}** - {command.help}" for command in cog.get_commands())

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help for `{command.qualified_name}`")

        embed.add_field(name="Usage", value=f"{command.qualified_name} {command.signature}", inline=False)
        embed.add_field(name="Description", value=command.help, inline=False)

        await self.get_destination().send(embed=embed)

def setup(bot):
  bot.help_command = HelpCommand()
