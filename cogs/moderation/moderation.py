# Moderation Commands

import discord
from discord.ext import commands


class Moderation(commands.Cog, name="Moderation"):
    """Startup Operations"""
    global testing_server

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="quit", alias=["logout", "shutdown", "kill"])
    async def quit_prefix(self, ctx: commands.Context) -> None:
        await ctx.message.delete()
        await self.bot.close()

    @discord.app_commands.command(name="quit")
    async def quit_slash(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Shutting down!", ephemeral=True)
        await self.bot.close()
    

async def setup(bot: commands.bot) -> None:
    await bot.add_cog(Moderation(bot))

