import json
from asyncio import TimeoutError
from math import floor, trunc

from discord import Attachment, Message
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.utils import oauth_url

from bot import SRBpp, execv


def time_format(time: float) -> str:
	hours = floor(time / 3600)
	minutes = floor((time % 3600) / 60)
	seconds = time % 60
	retime = ""

	if hours > 0:
		retime += f"{hours}:{'0' if minutes < 10 else ''}"
	retime += f"{minutes}:{'0' if seconds < 10 else ''}{round(seconds, 3)}"
	return retime


def _retime(start_time: float, end_time: float, framerate: int):
	frames = (
		(floor(end_time * framerate) / framerate)
		- (floor(start_time * framerate) / framerate)
	) * framerate

	seconds = round(frames / framerate * 1000) / 1000

	start_frame = trunc(start_time * framerate)
	end_frame = trunc(end_time * framerate)

	start_time = trunc(start_frame / framerate)
	end_time = trunc(end_frame / framerate)

	time = time_format(seconds)

	return f"Mod Note: Retimed (Start Frame: {start_frame}, End Frame: {end_frame}, FPS: {framerate}, Total Time: {time}"


class General(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	@commands.command(name="source")
	async def source(_, ctx: Context) -> None:
		"""
		Link the bots GitHub repository.
		"""
		SRC: str = "https://www.github.com/Mango0x45/speedrunbot-plusplus"
		await ctx.send(SRC)

	@commands.command(name="ping")
	async def ping(self, ctx: Context) -> None:
		"""
		Ping the bot, because why not?
		"""
		LATENCY: int = round(self.bot.latency * 1000)
		await ctx.send(f"Pong! {LATENCY}ms")

	@commands.command(name="invite")
	async def invite(self, ctx: Context) -> None:
		"""
		Get the bots discord invite link.
		"""
		await ctx.send(oauth_url(self.bot.user.id))

	@commands.command(name="retime")
	async def retime(self, ctx: Context, framerate: int = 30, *, data1=None):
		"""
		**UNSTABLE**
		Retime youtube videos using debugging data.
		This is a port of http://retime.mcbe.wtf/
		"""

		def check(msg: Message) -> bool:
			return (
				msg.author == ctx.author
				and msg.attachments[0]
				or len(msg.content) > 1000
			)

		file1: Attachment
		file2: Attachment
		data2: str
		start_time: float
		end_time: float
		try:
			if len(ctx.message.attachments) == 1 or data1:
				# First attachment will be the starting frame
				file1 = (
					ctx.message.attachments[0]
					if len(ctx.message.attachments)
					else None
				)
				if data1 or file1 and file1.size < 4_000:
					start_time = float(
						json.loads(data1 or await file1.read())["cmt"]
					)
				else:
					return await ctx.send("File is too large")

				await ctx.send("Awaiting second attachment")

				file2 = (
					await self.bot.wait_for("message", check=check, timeout=60)
				).attachments[0]
				if file2.size < 4_000:
					end_time = float(json.loads(await file2.read())["cmt"])
				else:
					return await ctx.send("File is too large")

			elif len(ctx.message.attachments) == 2:
				# First attachment will be the starting frame
				file1 = ctx.message.attachments[0]
				if file1.size < 4_000:
					start_time = float(json.loads(await file1.read())["cmt"])
				else:
					return await ctx.send("File is too large")

				file2 = ctx.message.attachments[2]
				if file2.size < 4_000:
					end_time = float(json.loads(await file2.read())["cmt"])
				else:
					return await ctx.send("File is too large")
			else:
				await ctx.send("Awaiting first attachment")
				msg1: Message = await self.bot.wait_for(
					"message", check=check, timeout=60
				)
				file1 = msg1.attachments[0] or msg1.content
				# First attachment will be the starting frame
				if file1.size < 4_000:
					start_time = float(
						json.loads(
							await file1.read()
							if type(
								file1 == "<class 'discord.message.Attachment'>"
							)
							else file1
						)["cmt"]
					)
				else:
					return await ctx.send("File is too large")

				await ctx.send("Awaiting second attachment")

				file2 = (
					await self.bot.wait_for("message", check=check, timeout=60)
				).attachments[0]
				if file2.size < 4_000:
					end_time = float(json.loads(await file2.read())["cmt"])
				else:
					return await ctx.send("File is too large")

			await ctx.send(_retime(start_time, end_time, framerate))
		except TimeoutError:
			await ctx.send("Waited for too long, aborting...")
		except Exception as e:
			raise e

	@commands.command(name="prefix", aliases=["prefixes"])
	async def prefix(self, ctx):
		"""
		Get the bot's prefixes
		"""
		prefixes = await self.bot.get_prefix(ctx.message)
		message = ""
		for prefix in prefixes:
			if "<@" in prefix:
				message = f"{prefix}, "
			else:
				message += f"`{prefix}`, "
		await ctx.send(f"My prefixes are: {message[:len(message) - 2]}")


def setup(bot: SRBpp) -> None:
	bot.add_cog(General(bot))
