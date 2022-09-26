import discord
import asyncio
from discord.ext import commands
from discord import app_commands
#from cogs.bash.util.BashView import BashView

import docker
'''
pip install pywin32==225
pip install docker
'''

class Bash(commands.GroupCog, name="bash"):
	"""
	Bash
	"""
	global testing_server

	#Connect to Docker api @tcp://localhost:2375
	client = docker.from_env()

	def __init__(self, bot: commands.bot):
		self.bot = bot

	async def run(self, command) -> str:
		#Build the image from the Dockerfile, might take a while if first time running
		built = self.client.images.build(path="./cogs/bash", tag="disc:v1")
		#Create a container from the newly created image and run the command
		ret = self.client.containers.run("disc:v1", command=["/bin/sh", "-c", command], remove=True)
		print(self.client.containers.list())
		#Decode and return result
		return str(ret.decode("utf-8"))

	@app_commands.command(name="start", description="Run commands in Ubuntu 22.04")
	async def bash(self, interaction: discord.Interaction, command: str) -> None:
		embed = discord.Embed()
		icon = "https://d1rytvr7gmk1sx.cloudfront.net/wp-content/uploads/2021/08/tux.jpg"
		embed.set_author(name="Ubuntu 22.04", icon_url=icon)
		embed.add_field(name=f"Running ~$ `{command}`", value="```...```", inline=False)

		await interaction.response.send_message(embed=embed)

		result = await self.run(command)
		embed = discord.Embed()
		embed.set_author(name="Ubuntu 22.04", icon_url=icon)
		embed.add_field(name=f"Ran ~$ `{command}`", value=f"```{result[:800]}```", inline=False)

		await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.bot) -> None:
	await bot.add_cog(Bash(bot), guilds=[discord.Object(id=250758983327940618)]) #change id