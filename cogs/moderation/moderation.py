# Moderation Commands

import discord
from discord.ext import commands
import os
from datetime import datetime

class Moderation(commands.Cog, name="Moderation"):
    """Startup Operations"""

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="quit", alias=["logout", "shutdown", "kill"])
    async def quit_prefix(self, ctx: commands.Context) -> None:
        if (self.bot.testing_server):
            await ctx.message.delete()
            await self.bot.close()
        else:
            await ctx.send(content="Bot not running in dev mode! (No tesing_server)")

    @discord.app_commands.command(name="quit")
    async def quit_slash(self, interaction: discord.Interaction) -> None:
        if (self.bot.testing_server):
            await interaction.response.send_message("Shutting down!", ephemeral=True)
            await self.bot.close()
        else:
            await interaction.response.send_message(content="Bot not running in dev mode! (No testing_server)", ephemeral=True)
    
    @discord.app_commands.command(name="updated")
    async def last_updates(self, interaction: discord.Interaction) -> None:
        '''
        Checks when bot was last updated on the server.
        '''
        file = os.path.join(os.getcwd(), ".git", "FETCH_HEAD")
        fetch = open(file, 'r')
        commit_hash = fetch.readline().split('\t')[0]
        time = os.path.getmtime(file)
        time = datetime.fromtimestamp(time).strftime('%m/%d/%Y %I:%M:%S')
        await interaction.response.send_message(content=f'Bot last updated on: {time} \nCommit Hash is: {commit_hash}', ephemeral=True)

async def setup(bot: commands.bot) -> None:
    await bot.add_cog(Moderation(bot))

