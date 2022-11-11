import discord

class PollInfoModal(discord.ui.Modal, title="Poll Information"):
	'''
	A modal (basically a form) for users to type the title, the options, and the
	timeout for a poll.
	'''
	max_num_options = 24

	'''
	Default fields for the modal
	'''
	title_field = discord.ui.TextInput(
		label = "Title",
		style=discord.TextStyle.short,
		placeholder="What to eat?",
		max_length=128
	)
	options_field = discord.ui.TextInput(
		label = "Poll Information",
		placeholder="poll option 1\npoll option 2\n...",
		style=discord.TextStyle.long
	)
	timeout_field = discord.ui.TextInput(
		label= "Timeout in minutes",
		style=discord.TextStyle.short,
		placeholder="How many minutes until poll times out?",
		default="5"
	)

	def __init__(self) -> None:
		self.poll_title = None
		self.poll_options = None
		self.poll_timeout = 5.0
		self.error = False
		self.embed = None
		super().__init__()

	async def on_submit(self, interaction:discord.Interaction) -> None:
		'''
		This function is called when the modal is submitted
		
		Parameters
		----------
		interaction: :class:`discord.Interaction`
			interaction of the submit button being clicked
		'''
		self.poll_title = self.title_field.value
		self.poll_options = self.options_field.value.split("\n")
		num_options = len(self.poll_options)
		if (num_options > PollInfoModal.max_num_options):
			raise OptionsOutOfRangeError(num_options, PollInfoModal.max_num_options) 
		self.poll_timeout = float(self.timeout_field.value)
		await interaction.response.defer()

	async def on_error(self, interaction:discord.Interaction, error:Exception) -> None:
		self.error = error
		embed = discord.Embed(title=f"**ERROR {error}**")
		embed.add_field(name="Title:", value=f"{self.title_field.value}", inline=False)
		embed.add_field(name="Options:", value=f"{self.options_field.value}", inline=False)
		embed.add_field(name="Timeout:", value=f"{self.timeout_field.value}", inline=False)
		print(type(error))
		if type(error) == OptionsOutOfRangeError:
			embed.set_field_at(index=1, name="**OPTIONS: TOO MANY OPTIONS**", value=f"{self.options_field.value}", inline=False)
		elif type(error) == ValueError:
			embed.set_field_at(index=2, name="**TIMEOUT: NOT A NUMBER**", value=f"{self.timeout_field.value}", inline=False)

		self.embed = embed
		await interaction.response.defer()
		self.stop()

class OptionsOutOfRangeError(Exception):
	'''
	Custom error for when the number of options exceeds the maximum

	Init Parameters	
	----------
	num_options:`int`
		The number of options
	max:`int`
		The maximum number of options

	TODO move to its own file
	'''
	def __init__(self, num_options:int, max:int) -> None:
		self.num_options = num_options
		self.max = max
		self.message = f"Number of options ({self.num_options}) > Max number of options ({self.max})"
		super().__init__()
	def __str__(self):
		return self.message