from code import InteractiveConsole, interact
from tkinter import Button
from typing import List
import discord

numbers = [ '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣' ]

class PollView(discord.ui.View):
	def __init__(self, title: str = None, content: List[str] = None, embed: discord.Embed = None) -> None:
		self.title = title
		self.embed = embed
		super().__init__()
		for i in range(len(content)):
			button = discord.ui.Button(style=discord.ButtonStyle.blurple, label=str(i))
			# emoji=discord.PartialEmoji.from_str(numbers[i]))
			button.callback = self.buttonc
			self.add_item(button)

	async def buttonc(self, interaction: discord.Interaction) -> None:
		print(interaction.data)
		self.embed.set_field_at(0, name="owo", value="owo2", inline=False)
		await interaction.response.edit_message(embed=self.embed)
		# await interaction.edit_original_response(embed=self.embed)

	# @discord.ui.button(label="Title", style=discord.ButtonStyle.blurple)
	# async def create(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
	# 	print(interaction)