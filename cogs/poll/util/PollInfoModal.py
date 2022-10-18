import os
import asyncio
import time
from cogs.poll.util.PollView import PollView
import random
import discord


class PollInfoModal(discord.ui.Modal, title="Poll Information"):
	max_num_options = 24
	poll_title = discord.ui.TextInput(
		label = "Title",
		style=discord.TextStyle.short,
		placeholder="What to eat?",
		max_length=128
	)
	poll_information = discord.ui.TextInput(
		label = "Poll Information",
		placeholder="poll option 1\npoll option 2\n...",
		style=discord.TextStyle.long
	)
	poll_timeout = discord.ui.TextInput(
		label= "Timeout in minutes",
		style=discord.TextStyle.short,
		placeholder="How many minutes until poll times out?",
		default="5"
	)

	def __init__(self, title: str = None) -> None:
		self.poll_title.default = title
		super().__init__()

	async def on_submit(self, interaction: discord.Interaction) -> None:
		'''
		This function is called when the modal submits the
		'''
		# TODO add error checking for non float timeouts
		title = self.poll_title.value
		content = self.poll_information.value.split("\n")
		send_followup = False
		if (len(content) > PollInfoModal.max_num_options):
			send_followup = True
			content = content[:PollInfoModal.max_num_options]

		poll_id = f"{hex(int(time.time()))[2:]}={hex(random.randrange(0, 4294967295))[2:]}"
		embed = discord.Embed(title=title, type="rich")
		embed.set_author(name=interaction.user.nick, icon_url=interaction.user.display_avatar.url)
		for i in range(len(content)):
			embed.add_field(name=PollView.number_emojis[i], value=f"**{content[i]}**")
		
		view = PollView(
			title=title,
			content=content,
			embed=embed,
			timeout=float(self.poll_timeout.value),
			poll_id=poll_id
		)
		# TODO maybe ID looks better as an embed footer?
		await interaction.response.send_message(
			embed=embed,
			view=view,
			content=f"ID:{poll_id}"
		)
		if send_followup:
			await interaction.followup.send(
				ephemeral=True,
				content=f"You can't have more than {PollInfoModal.max_num_options} options, limiting to {PollInfoModal.max_num_options}."
			)
		
		# Wait for the poll to end which creates a barplot with the "{poll_id}.png" as the name
		filename = f"{poll_id}.png"
		while not(filename in os.listdir(os.getcwd())):
			await asyncio.sleep(1)
		await interaction.followup.send(file=discord.File(filename))
		os.remove(os.path.join(os.getcwd(), filename))