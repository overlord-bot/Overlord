import discord
import asyncio
from discord.ext import commands
from discord import app_commands

import docker

class Bash(commands.GroupCog, name="bash"):
	"""
	Bash
	"""
	global testing_server

	client = docker.from_env()

	def __init__(self, bot: commands.bot):
		self.bot = bot

	async def run(self, command) -> str:
		built = self.client.images.build(path="./cogs/bash", tag="disc:v1")
		ret = self.client.containers.run("disc:v1", command=["/bin/sh", "-c", command], remove=True)
		print(self.client.containers.list())
		return str(ret.decode("utf-8"))

	@app_commands.command(name="start", description="Run commands in Ubuntu 22.04")
	async def bash(self, interaction: discord.Interaction, command: str) -> None:
		embed = discord.Embed()
		icon = "https://d1rytvr7gmk1sx.cloudfront.net/wp-content/uploads/2021/08/tux.jpg"
		embed.set_author(name="Ubuntu 22.04", icon_url=icon)
		embed.add_field(name="Running ~$ `" + command + "`", value="```...```", inline=False)

		await interaction.response.send_message(embed=embed)

		result = await self.run(command)
		embed = discord.Embed()
		embed.set_author(name="Ubuntu 22.04", icon_url=icon)
		embed.add_field(name="Ran ~$ `" + command + "`", value="```" + result[:800] + "```", inline=False)

		await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.bot) -> None:
	await bot.add_cog(Bash(bot), guilds=[discord.Object(id=250758983327940618)]) #change id