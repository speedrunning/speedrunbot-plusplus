import json
from asyncio import TimeoutError
from math import floor, trunc
from typing import Literal, Optional, Union

import cryptocode
from discord import Embed, Forbidden, Message, User
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.utils import oauth_url
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

from bot import SRBpp, run_and_output
from cogs.src import PREFIX as SRC_PREFIX

SRC_NAMESPACE = SRC_PREFIX.split("/")[0]
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

	@commands.group(name="link")
	async def link(self, ctx: Context):
		"""
		Link an external account to your discord account via this bot.
		"""
		if ctx.invoked_subcommand is None:
			await ctx.send("Invalid service passed.")

	@link.command(name="sr.c", aliases=["src"])
	async def link_src(self, ctx, apikey: str):

		try:
			await ctx.message.delete()
		except Forbidden:
			await ctx.reply(
				"Please delete this message or someone could take control of your speedrun.com user"
			)

		user = str(hash(ctx.author))

		async with self.bot.session.get(
			"https://www.speedrun.com/api/v1/profile",
			headers={
				"X-API-Key": apikey,
			},
		) as r:

			# As soon as we're done with the api key
			# Delete it from memory
			del apikey

			if not r.ok:
				print(r.status, await r.text())
				return await ctx.reply("Something went wrong, please try again later.")

			res = await r.json()
			src_id = cryptocode.encrypt(res["data"]["id"], str(ctx.author.id))

			self.bot.redis.hset("users", key=f"{user}.{SRC_NAMESPACE}", value=src_id)

			await ctx.send(
				f"Linked {ctx.author.mention} to {res['data']['names']['international']}"
			)

	@commands.group(aliases=("profile",))
	async def whois(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send("Invalid service passed")

	@whois.command(name="src")
	async def whois_src(self, ctx, user: Optional[str] = None):
		if user:
			try:
				user = await commands.UserConverter().convert(ctx, user)
			except commands.errors.UserNotFound:
				pass
		else:
			user = ctx.author
		await run_and_output(ctx, f"{SRC_PREFIX}/whois", user, title=f"Info about {user}")


def setup(bot: SRBpp) -> None:
	bot.add_cog(General(bot))
