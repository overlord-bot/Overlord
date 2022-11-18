import asyncio, os, discord
from discord.ext import commands
from .util.PollInfoModal import PollInfoModal
from .util.PollView import PollView
from utils.SemiRandID import generate_semi_rand_id

class Polls(commands.GroupCog, name="polls"):
	'''
	Interactive polls that update based on who answered.
	'''
	def __init__(self, bot: commands.bot):
		self.bot = bot

	@discord.app_commands.command(name="create")
	async def create(self, interaction:discord.Interaction) -> None:
		'''
		Creates a poll.

		Parameters
		----------
		interaction: :class:`discord.Interaction`
			The interaction that triggered this slash command.
		'''

		# Create a modal to send (basically a form) to collect information from the user
		modal = PollInfoModal()
		await interaction.response.send_modal(modal)
		await modal.wait()

		if (modal.error):
			await interaction.followup.send(embed=modal.embed, ephemeral=True)
			return

		# Creates an almost unique id for poll
		poll_id:str = generate_semi_rand_id()

		# Create an embed and add all the fields
		embed:discord.Embed = await self.generate_embed(interaction=interaction, modal=modal)
		embed.set_footer(text=f"ID:{poll_id}", icon_url=None)
		
		view = PollView(
			title=modal.poll_title,
			content=modal.poll_options,
			embed=embed, 
			timeout=modal.poll_timeout,
			poll_id=poll_id
		)
		
		await interaction.followup.send(embed=embed, view=view, content=f"{modal.poll_title}")
		await view.wait()

		# Wait for the poll to end which creates a barplot with the "{poll_id}.png" as the name
		# TODO might be a better way to do this
		filename = f"{poll_id}.png"
		while not(filename in os.listdir(os.getcwd())):
			await asyncio.sleep(1)
		await interaction.followup.send(file=discord.File(filename))
		os.remove(os.path.join(os.getcwd(), filename))

	async def generate_embed(self, interaction:discord.Interaction, modal:PollInfoModal):
		'''
		TODO finish
		'''

		# TODO randomize embed color?
		# discord.Color(255)
		# colour="FF00B5",
		embed = discord.Embed(title=modal.poll_title, type="rich")
		embed.set_author(name=interaction.user.nick, icon_url=interaction.user.display_avatar.url)
		for i in range(len(modal.poll_options)):
			embed.add_field(name=PollView.number_emojis[i], value=f"**{modal.poll_options[i]}**", inline=False)
		return embed


async def setup(bot: commands.bot) -> None:
	await bot.add_cog(Polls(bot))