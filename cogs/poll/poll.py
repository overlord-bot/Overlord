import asyncio
import os
import discord, time, random
from discord.ext import commands
from .util.PollInfoModal import PollInfoModal
from .util.PollView import PollView

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
		# send_followup_msg = False
    
		# Create a modal to send (basically a form) to collect information
		# 	from the user
		modal = PollInfoModal()
		await interaction.response.send_modal(modal)
		await modal.wait()

		if (modal.error):
			await self.send_error_message(interaction=interaction, embed=modal.embed)
			return
			# send_followup_msg = True
			# content = content[:PollInfoModal.max_num_options]

		# Creates an almost unique id for poll
		poll_id = f"{hex(int(time.time()))[2:]}={hex(random.randrange(0, 4294967295))[2:]}"

		# Create an embed and add all the fields
		# TODO randomize embed color?
		# discord.Color(255)
		# colour="FF00B5",
		embed = discord.Embed(title=modal.poll_title, type="rich")
		embed.set_author(name=interaction.user.nick, icon_url=interaction.user.display_avatar.url)
		for i in range(len(modal.poll_options)):
			embed.add_field(name=PollView.number_emojis[i], value=f"**{modal.poll_options[i]}**", inline=False)
		
		view = PollView(
			title=modal.poll_title,
			content=modal.poll_options,
			embed=embed, 
			timeout=modal.poll_timeout,
			poll_id=poll_id
		)
		

		await interaction.followup.send(
						embed=embed, view=view, content=f"ID:{poll_id}"
		)

		# if send_followup_msg:
		# 	await interaction.followup.send(
		# 					ephemeral=True,
		# 					content=f"You can't have more than {PollInfoModal.max_num_options} \
		# 										options, limiting to {PollInfoModal.max_num_options}."
		# 	)
		
		# Wait for the poll to end which creates a barplot with the "{poll_id}.png" as the name
		# TODO might be a better way to do this
		await view.wait()
		filename = f"{poll_id}.png"
		while not(filename in os.listdir(os.getcwd())):
			await asyncio.sleep(1)
		await interaction.followup.send(file=discord.File(filename))
		os.remove(os.path.join(os.getcwd(), filename))

	async def send_error_message(self, interaction:discord.Interaction, embed:discord.Embed) -> None:
		await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.bot) -> None:
	await bot.add_cog(Polls(bot))