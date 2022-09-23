import discord
from discord.ext import commands
from cogs.poll.util.PollView import PollView

class Polls(commands.GroupCog, name="polls"):
	"""
	Interactive polls that update based on who answered.
	"""
	def __init__(self, bot: commands.bot):
		self.bot = bot

	@discord.app_commands.command(name="create")
	async def poll(self, interaction: discord.Interaction, poll_title: str, *, args: str) -> None:
		# discord.Color(255)
		# colour="FF00B5",
		embed = discord.Embed(title=poll_title)
		embed.set_footer(text="Hi:" + "#".join(args), icon_url=None)
		view = PollView()
		await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.bot) -> None:
	await bot.add_cog(Polls(bot), guilds=[discord.Object(id=333409598365106176)])