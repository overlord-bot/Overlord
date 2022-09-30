# Go minigame

from discord.ext import commands

class GoMinigame(commands.Cog, name = "Go"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def go(self, context):
        await context.send("'!go' command working!")

async def setup(bot):
    await bot.add_cog(GoMinigame(bot))