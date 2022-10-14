import discord
from discord.ext import commands
from cogs.poll.util.PollInfoModal import PollInfoModal

class Polls(commands.GroupCog, name="polls"):
	"""
	Interactive polls that update based on who answered.
	"""
	def __init__(self, bot: commands.bot):
		self.bot = bot

	@discord.app_commands.command(name="create")
	async def poll(self, interaction: discord.Interaction) -> None:
		# TODO randomize embed color?
		# discord.Color(255)
		# colour="FF00B5",
		modal = PollInfoModal()
		await interaction.response.send_modal(modal)

async def setup(bot: commands.bot) -> None:
	await bot.add_cog(Polls(bot), guilds=[discord.Object(id=333409598365106176)])