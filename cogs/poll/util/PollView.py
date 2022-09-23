import discord

class PollView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__()
		self.value = None

	@discord.ui.button(label="Title", style=discord.ButtonStyle.blurple)
	async def create(self, button: discord.ui.Button, interaction: discord.Interaction):
		# AttributeError: 'Button' object has no attribute 'response'
		await interaction.response.send_message("h")
