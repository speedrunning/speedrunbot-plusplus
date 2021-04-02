import json
from asyncio import TimeoutError
from math import floor, trunc

from discord import Attachment, Message
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.utils import oauth_url

from bot import SRBpp, run_and_output

PREFIX = "general/"


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
	async def retime(
		self,
		ctx: Context,
		framerate: int = 30,
		data1: str = None,
		data2: str = None,
	):
		"""
		**UNSTABLE**
		Retime youtube videos using debugging data.
		This is a port of http://retime.mcbe.wtf/
		"""

		def check(msg: Message) -> bool:
			return msg.author == ctx.author

		try:
			if not (data1 and data2):
				if len(ctx.message.attachments) == 0:
					await ctx.send("Waiting first input...")
					msg1: Message = await self.bot.wait_for(
						"message", check=check, timeout=60
					)
					if len(msg1.attachments) == 1:
						data1 = (await msg1.attachments[0].read()).decode("utf-8")
					else:
						data1 = msg1.content
					await ctx.send("Waiting second input...")
					msg2 = await self.bot.wait_for(
						"message", check=check, timeout=60
					)
					if len(msg2.attachments) == 1:
						data2 = (await msg2.attachments[0].read()).decode("utf-8")
					else:
						data2 = msg2.content
				elif len(ctx.message.attachments) == 1:
					data1 = (await ctx.message.attachments[0].read()).decode(
						"utf-8"
					)
					await ctx.send("Waiting second input...")
					msg2 = await self.bot.wait_for(
						"message", check=check, timeout=60
					)
					if len(msg2.attachments) == 1:
						data2 = (await msg2.attachments[0].read()).decode("utf-8")
					else:
						data2 = msg2.content
				elif len(ctx.message.attachments) == 2:
					data1 = (await ctx.message.attachments[0].read()).decode(
						"utf-8"
					)
					data2 = (await ctx.message.attachments[1].read()).decode(
						"utf-8"
					)
			elif data1 and not data2:
				await ctx.send("Waiting second input...")
				msg2 = await self.bot.wait_for(
					"message", check=check, timeout=60
				)
				if len(msg2.attachments) == 1:
					data2 = (await msg2.attachments[0].read()).decode("utf-8")
				else:
					data2 = msg2.content
		except Exception as e:
			raise e

		await run_and_output(
			ctx,
			f"{PREFIX}/retime.py",
			str(framerate),
			data1,
			data2,
			TITLE="Retimed!",
		)

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
