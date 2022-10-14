import discord
import asyncio
from discord.ext import commands
from discord import app_commands

'''
pip install pywin32==225
pip install docker
'''
from textwrap import wrap
import docker
from importlib.metadata import version
import platform

if platform.system() == 'Windows' and int(version('pywin32')) > 225:
	raise Exception('The Docker Python package requires pywin32 <= ver 225 to run, please downgrade or run on Linux')

class Bash(commands.GroupCog, name="bash"):
	"""
	Bash - Allows for running linux programs inside discord by creating and executing commands inside Docker containers
	"""
	global testing_server

	try:
		#Connect to Docker api @tcp://localhost:2375
		client = docker.from_env()
		print("Bulding Docker Image...")
		#Build the image from the Dockerfile, might take a while if first time running
		built = client.images.build(path="./cogs/bash", tag="disc:v1")
		print("Docker Image built as disc:v1")
	except Exception as err:
		raise Exception(err)

	def __init__(self, bot: commands.bot):
		self.bot = bot

	async def run(self, command) -> str:
		try:
			print(command)
			#Create a container from the newly created image and run the command
			ret = self.client.containers.run("disc:v1", command=["/bin/sh", "-c", command], remove=True)
			#Decode result (bytes -> str)
			ret = str(ret.decode("utf-8"))
		except Exception as err:
			#Catch and print errors
			print(err)
			s = err.stderr
			ret = s.decode("utf-8")
		print(self.client.containers.list())
		return ret

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
	test_server = 0 #place test server id here
	await bot.add_cog(Bash(bot), guilds=[discord.Object(id=test_server)])