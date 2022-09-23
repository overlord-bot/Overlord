import discord

class PollView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__()
		self.value = None

	@discord.ui.button(label="Title", style=discord.ButtonStyle.blurple)
	async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
		print(interaction)
		await interaction.response.send_message("h")
