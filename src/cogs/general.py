import json
from asyncio import TimeoutError
from math import floor, trunc
from typing import Literal, Union

from discord import Embed, Message
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.utils import oauth_url
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

from bot import SRBpp, run_and_output

PREFIX: Literal["general/bin"] = "general/bin"


class General(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot = bot

	async def source(_, ctx: Union[Context, SlashContext]) -> None:
		"""
		Link the bots GitHub repository.
		"""
		await ctx.send("https://www.github.com/Mango0x45/speedrunbot-plusplus")

	@cog_ext.cog_slash(
		name="source",
		description="Link the bots GitHub repository.",
	)
	async def source_slash(self, ctx: SlashContext) -> None:
		await self.source(ctx)

	@commands.command(name="source")
	async def source_bot(self, ctx: Context) -> None:
		"""
		Link the bots GitHub repository.
		"""
		await self.source(ctx)

	async def ping(self, ctx: Union[Context, SlashContext]) -> None:
		await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

	@cog_ext.cog_slash(
		name="ping",
		description="Ping the bot, because why not?",
	)
	async def ping_slash(self, ctx: SlashContext):
		await self.ping(ctx)

	@commands.command(name="ping")
	async def ping_bot(self, ctx: Context):
		"""
		Ping the bot, because why not?
		"""
		await self.ping(ctx)

	async def invite(self, ctx: Union[Context, SlashContext]) -> None:
		"""
		Get the bots discord invite link.
		"""
		embed = Embed(title="Invite this bot to your server!")
		embed.add_field(
			name="As a bot with slash commands",
			value=f"[Click here]({oauth_url(self.bot.user.id, scopes=('bot', 'applications.commands'))})",
		)
		embed.add_field(
			name="As a bot **without** slash commands",
			value=f"[Click here]({oauth_url(self.bot.user.id)})",
		)
		embed.add_field(
			name="As an interaction with  **only** slash commands",
			value=f"[Click here]({oauth_url(self.bot.user.id, scopes=('applications.commands',))})",
		)
		await ctx.send(embed=embed)

	@cog_ext.cog_slash(
		name="invite",
		description="Get the bots discord invite link.",
	)
	async def invite_slash(self, ctx: SlashContext) -> None:
		await self.invite(ctx)

	@commands.command(name="invite")
	async def invite_bot(self, ctx: Context) -> None:
		"""
		Get the bots discord invite link.
		"""
		await self.invite(ctx)

	@commands.command(name="retime")
	async def retime_bot(
		self,
		ctx: Context,
		framerate: int = 30,
		data1: str = None,
		data2: str = None,
	) -> None:
		"""
		**UNSTABLE**
		Retime youtube videos using debugging data.
		This is a port of http://retime.mcbe.wtf/
		"""

		msg1: Message
		msg2: Message

		def check(msg: Message) -> bool:
			return msg.author == ctx.author and msg.channel == ctx.channel

		try:
			if not (data1 and data2):
				if len(ctx.message.attachments) == 0:
					await ctx.send("Waiting for first input...")
					msg1 = await self.bot.wait_for("message", check=check, timeout=60)
					if len(msg1.attachments) == 1 and msg1.attachments[0].size < 4_000_000:
						data1 = (await msg1.attachments[0].read()).decode("utf-8")
					else:
						data1 = msg1.content
					await ctx.send("Waiting for second input...")
					msg2 = await self.bot.wait_for("message", check=check, timeout=60)
					if len(msg2.attachments) == 1 and msg2.attachments[0].size < 4_000_000:
						data2 = (await msg2.attachments[0].read()).decode("utf-8")
					else:
						data2 = msg2.content
				elif (
					len(ctx.message.attachments) == 1
					and ctx.message.attachments[0].size < 4_000_000
				):
					data1 = (await ctx.message.attachments[0].read()).decode("utf-8")
					await ctx.send("Waiting for second input...")
					msg2 = await self.bot.wait_for("message", check=check, timeout=60)
					if len(msg2.attachments) == 1 and msg2.attachments[0].size < 4_000_000:
						data2 = (await msg2.attachments[0].read()).decode("utf-8")
					else:
						data2 = msg2.content
				elif (
					len(ctx.message.attachments) == 2
					and ctx.message.attachments[0].size < 4_000_000
					and ctx.message.attachments[1].size < 4_000_000
				):
					data1 = (await ctx.message.attachments[0].read()).decode("utf-8")
					data2 = (await ctx.message.attachments[1].read()).decode("utf-8")
			elif data1 and not data2:
				await ctx.send("Waiting for second input...")
				msg2 = await self.bot.wait_for("message", check=check, timeout=60)
				if len(msg2.attachments) == 1 and msg2.attachments[0].size < 4_000_000:
					data2 = (await msg2.attachments[0].read()).decode("utf-8")
				else:
					data2 = msg2.content
		except TimeoutError:
			return await ctx.send("Waited for too long. Aborting...")

		await run_and_output(
			ctx,
			f"{PREFIX}/retime",
			str(framerate),
			data1,
			data2,
			title="Retimed!",
		)

	@commands.command(name="prefix", aliases=("prefixes",))
	async def prefix_bot(self, ctx: Context) -> None:
		"""
		Get the bot's prefixes.
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
