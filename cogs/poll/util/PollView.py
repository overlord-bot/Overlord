import discord
import matplotlib.pyplot as plt
from typing import List


class PollView(discord.ui.View):
	'''
	This poll view contains the buttons to vote on specific options for a poll.
	'''

	'''
	Static Variables
	'''
	# TODO optimize the code to only use a list of number_emojis of size 10
	number_emojis = [ 
    '0️⃣1️⃣', '0️⃣2️⃣', '0️⃣3️⃣', '0️⃣4️⃣', '0️⃣5️⃣',
		'0️⃣6️⃣', '0️⃣7️⃣', '0️⃣8️⃣', '0️⃣9️⃣', '1️⃣0️⃣',
		'1️⃣1️⃣', '1️⃣2️⃣', '1️⃣3️⃣', '1️⃣4️⃣', '1️⃣5️⃣',
		'1️⃣6️⃣', '1️⃣7️⃣', '1️⃣8️⃣', '1️⃣9️⃣', '2️⃣0️⃣',
		'2️⃣1️⃣', '2️⃣2️⃣', '2️⃣3️⃣', '2️⃣4️⃣', '2️⃣5️⃣'
  ]
    
	def __init__(self, title:str, content:List[str], embed:discord.Embed, timeout:int, poll_id:str) -> None:
		self.title = title
		self.content = content
		self.embed = embed
		self.num_polls = len(content)
		self.voted = [[] for i in range(self.num_polls)]
		self.poll_id = poll_id
		super().__init__(timeout=60*timeout)

		# Generate buttons based on how many options
		for i in range(self.num_polls):
			button = discord.ui.Button(
				custom_id=f"{self.poll_id}:{i}",
				style=discord.ButtonStyle.blurple,
			  label=PollView.number_emojis[i]
			)
			button.callback = self.button_callback
			self.add_item(button)
		
		# Create an "End Poll" button
		button = discord.ui.Button(
			custom_id=f"{self.poll_id}:-2",
			style=discord.ButtonStyle.red,
			label="End Poll"
		)
		button.callback = self.end_button_callback
		self.add_item(button)

	async def check_poll_helper(self, id:str) -> int:
		'''
		Checks to see if the id of a button that is clicked is
			corresponds with this poll.

		Parameters
		----------
		id: :class:`str`
			the id of a poll and button id delimited by a colon.
			Example: "{poll_id}:{button_id}"

		Returns
		-------
		`button_id` if button corresponds with this poll and is not the end poll button

		`-2` if button corresponds with this poll and is the end poll button

		`-1` if neither
		'''
		delimiter_idx = id.index(":")
		poll_id = id[:delimiter_idx]
		if (poll_id != self.poll_id):
			return -1
		return int(id[delimiter_idx+1:])
		
	async def button_callback(self, interaction:discord.Interaction) -> None:
		'''
		When a numbered button is clicked, this callback function is called.
		
		Parameters
		----------
		interaction: :class:`discord.Interaction`
			The interaction from a button click
		'''

		# Check to see if the button clicked corresponds with this poll
		button_id = await self.check_poll_helper(interaction.data["custom_id"]) 
		if button_id < 0:
			return

		# Add or remove the user from the option clicked
		if interaction.user in self.voted[button_id]:
			self.voted[button_id].remove(interaction.user)
		else:
			self.voted[button_id].append(interaction.user)

		# Update the users who voted on this option on the embed and
		# edit the message with the new embed
		self.embed.set_field_at(
			index=button_id,
			name=self.embed.fields[button_id].name,
			value=f"**{self.content[button_id]}**\n" +
						"\n".join(map(lambda user: user.display_name, self.voted[button_id]))
			)
		await interaction.response.edit_message(embed=self.embed)

	async def end_button_callback(self, interaction:discord.Interaction) -> None:
		'''
		When the "End Poll" button is clicked, this callback function is called.

		Parameters
		----------
		interaction: :class:`discord.Interaction`
			Interaction of a button click
		'''
		# Check to see if the button clicked corresponds with this poll
		button_id = await self.check_poll_helper(interaction.data["custom_id"]) 
		if button_id != -2:
			return

		print(f"Poll {self.poll_id}:{self.title} has been ended by {interaction.user.display_name}.")
		# Defering is needed to stop "Interaction has not responded" error message
		await interaction.response.defer() 
		# The buttons are visually removed in poll.py, this removes the objects so they can't be interacted with
		self.clear_items() 
		self.stop()
		
	async def on_timeout(self) -> None:
		'''
		This function is called when the poll times out.
		'''
		print(f"Poll {self.poll_id}:{self.title} timed out.")
		# The buttons are visually removed in poll.py, this removes the objects so they can't be interacted with
		self.clear_items()

	async def create_plot(self) -> None:
		'''
		Create a bar plot and save it with the name "poll_id.png"
		'''
		count = [len(poll) for poll in self.voted]
		plt.title(label=self.title)
		# TODO make each bar a random color
		# color_arr = [
		# 	(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
		# 	for i in range()
		# ]
		plt.bar(x=self.content, height=count)
		plt.yticks(ticks=[i for i in range(max(count)+1)])
		plt.savefig(f'{self.poll_id}.png')
		plt.close()