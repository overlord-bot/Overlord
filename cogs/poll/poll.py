import discord
from discord.ext import commands
from cogs.poll.util.PollInfoModal import PollInfoModal

class Polls(commands.GroupCog, name="polls"):
	'''
	Interactive polls that update based on who answered.
	'''
	def __init__(self, bot: commands.bot):
		self.bot = bot

	@discord.app_commands.command(name="create")
	async def create(self, interaction: discord.Interaction) -> None:
		'''
		Creates a poll.
		'''
    
		# Create a modal to send (basically a form) to collect information
		# from the user
		modal = PollInfoModal()
		await interaction.response.send_modal(modal)

async def setup(bot: commands.bot) -> None:
	await bot.add_cog(Polls(bot))