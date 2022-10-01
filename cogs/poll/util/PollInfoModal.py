from code import interact
from cogs.poll.util.PollView import PollView
import discord

class PollInfoModal(discord.ui.Modal, title="Poll Information"):
	poll_title = discord.ui.TextInput(
		label = "Title",
		style=discord.TextStyle.short,
		placeholder="What to eat?",
		max_length=128
	)
	poll_information = discord.ui.TextInput(
		label = "Poll Information",
		style=discord.TextStyle.long	
	)

	# appliedcsskills.withgoogle.com
	# g.co/techdevguide
	# g.co/buildyourfuture

	def __init__(self, title: str = None) -> None:
		self.poll_title.default = title
		super().__init__()

	async def add_item(self) -> None:
		item = discord.ui.TextInput(label="Item")
		return super().add_item(item)

	async def on_submit(self, interaction: discord.Interaction) -> None:
		title = self.poll_title.default
		content = self.poll_information.value.split("\n")
		print(content)
		embed = discord.Embed(title=title)
		embed.set_author(name=interaction.user.nick, icon_url=interaction.user.display_avatar.url)
		for i in range(len(content)):
			embed.add_field(name=str(i), value=content[i])
		view = PollView(title=title, content=content)
		await interaction.response.send_message(embed=embed, view=view)
		# await interaction.response.send_message(content="Thanks")
