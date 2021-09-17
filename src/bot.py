import asyncio
import json
import os
import shlex
from datetime import datetime
from pathlib import Path
from sys import stderr
from typing import Generator, Literal, Optional, Union

import cryptocode
import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message
from discord_slash import SlashCommand, SlashContext
from redis import Redis

PREFIX = Path(__file__).parent
ROOT_DIR = f"{PREFIX}/.."
EXTENSIONS = (f"cogs.{f[:-3]}" for f in os.listdir(f"{PREFIX}/cogs") if f.endswith(".py"))


class Executed:
	def __init__(self, returncode: int, stdout: bytes, stderr: bytes) -> None:
		self.returncode = returncode
		self._stdout = stdout
		self._stderr = stderr

	@property
	def stdout(self) -> str:
		return self._stdout.decode()

	@property
	def stderr(self) -> str:
		return self._stderr.decode()


def divide_chunks(l: list[str], n: int) -> Generator[list[str], None, None]:
	"""
	Take a list of strings and return a generator which yields the same list of strings but in
	chunks of `n` strings.
	"""
	for i in range(0, len(l), n):
		yield l[i : i + n]


async def execv(prog: str, *argv: tuple[str, ...]) -> Executed:
	"""
	Run a program called PROG with the command line arguments ARGV. This returns a tuple
	containing the processes returncode, as well as the encoded stdout and stderr.
	"""
	# This is like `shlex.join()`, but it gets rid of any `None` values.
	args = " ".join(shlex.quote(arg) for arg in tuple(filter(lambda x: x, argv)))

	ret = await asyncio.create_subprocess_shell(
		f"{PREFIX}/{prog} {args}", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
	)
	stdout, stderr = await ret.communicate()
	return Executed(ret.returncode, stdout, stderr)


async def run_and_output(
	ctx: Union[SlashContext, Context],
	prog: str,
	*argv: tuple[str, discord.User, ...],
	title: Optional[str] = None,
) -> None:
	"""
	Run a program called `prog` with the command line arguments `argv` as a subprocess and
	return its output + exit code. If `title` is supplied, it will be used as the title of the
	embed that is sent to discord. If `title` is not supplied, then the first line of output
	from `prog` will be used.
	"""
	prog_namespace = prog.split("/")[0]
	args = list(argv)
	for arg in range(len(args)):
		if isinstance(args[arg], discord.User) or isinstance(args[arg], discord.Member):
			user_prog_id_hashed = ctx.bot.redis.hget("users", f"{hash(args[arg])}.{prog_namespace}")
			if user_prog_id_hashed:
				user_prog_id = cryptocode.decrypt(user_prog_id_hashed, str(ctx.author.id))
				if user_prog_id:
					args.pop(arg)
					args.insert(arg, user_prog_id)
					args.insert(arg, "-u")
			else:
				args[arg] = args[arg].name
	is_slash_called = isinstance(ctx, SlashContext)
	if is_slash_called:
		await ctx.defer()
	else:
		await ctx.trigger_typing()

	process = await execv(prog, *args)
	if process.returncode != 0:
		await ctx.reply(process.stderr)
		return

	title, desc = process.stdout.split("\n", 1) if not title else [title, process.stdout]

	# If the first line of the description begins with the string "__THUMBNAIL__: " then we take
	# the following link and make that the embed thumbnail
	if desc.startswith("__THUMBNAIL__: "):
		thumbnail, desc = desc.split("\n", 1)
		thumbnail = thumbnail.replace("__THUMBNAIL__: ", "", 1)
	else:
		thumbnail = None

	if len(desc) > 2000:
		lines = list(divide_chunks(desc.split("\n"), 15))
		lines_length = len(lines)
		try:
			if is_slash_called:
				try:
					await ctx.author.send("")
				except discord.Forbidden:
					await ctx.send(
						"The contents of this message are too long, and as such they cannot be sent"
						" through a slash command. Please try again using a regular command."
					)
					return
				except discord.HTTPException:
					await ctx.reply(
						"The contents of this message are too long and as such they will be sent"
						" in DMs"
					)
			else:
				await ctx.reply(
					"The contents of this message are too long and as such they will be sent in DMs"
				)
			async with ctx.author.typing():
				for line in range(lines_length):
					embed = discord.Embed(
						title=f"{title} Page: {line + 1}/{lines_length}",
						description="\n".join(lines[line]),
					)
					if thumbnail:
						embed.set_thumbnail(url=thumbnail)
					await ctx.author.send(embed=embed)
		except discord.Forbidden:
			await ctx.reply(
				"You have blocked the bot and the message is too long to be sent in this channel."
				" Please unblock me and try again."
			)
	else:
		embed = discord.Embed(title=title, description=desc)
		if thumbnail:
			embed.set_thumbnail(url=thumbnail)
		if is_slash_called:
			await ctx.send(embed=embed)
		# If the original message is replying to another message then try to reply to that message
		elif ctx.message.reference:
			# If the message is in cache then reply to it
			if ctx.message.reference.cached_message:
				# If the message is deleted then just reply to the message that invoked the
				# command
				if ctx.message.reference.cached_message.fail_if_not_exists:
					await ctx.reply(embed=embed)
				else:
					await ctx.message.reference.cached_message.reply(embed=embed)
			# If it's not cached then get the message then reply to it
			else:
				msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
				await msg.reply(embed=embed)
		else:
			await ctx.reply(embed=embed)


class SRBpp(commands.Bot):
	def __init__(self) -> None:
		super().__init__(
			allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False),
			case_insensitive=True,
			command_prefix=get_prefix,
			intents=discord.Intents(messages=True, guilds=True),
			help_command=commands.MinimalHelpCommand(dm_help=True),
			activity=discord.Game("+help / ;help"),
		)

		slash = SlashCommand(self, sync_commands=True, sync_on_cog_reload=True)

		for extension in EXTENSIONS:
			try:
				self.load_extension(extension)
			except Exception as e:
				print(e, file=stderr)

		config = {}
		try:
			f = open(f"{ROOT_DIR}/config.json", encoding="utf-8")
			config = json.load(f)
			self.token = config["token"]
		except IOError:
			print("No config file found, trying backwards compatible method.")
			try:
				f = open(f"{ROOT_DIR}/token", "r", encoding="utf-8")
				self.token = f.read().strip()
			except IOError:
				print("No bot token found. ")
				exit(1)
		finally:
			f.close()

		if not config:
			print("Please create a config.json file.")
			exit(1)

		self.redis = Redis(
			host=config["redis_hostname"] if "redis_hostname" in config else "localhost",
			port=config["redis_port"] if "redis_port" in config else 6379,
			db=(config["redis_db"] if "redis_db" in config else 0),
			decode_responses=True,
		)

	async def on_ready(self) -> None:
		"""
		Code to run when the bot starts up.
		"""
		self.uptime = datetime.utcnow()
		self.session = ClientSession()

		print(
			f"Bot Name\t\t{self.user.name}\n"
			+ f"Bot ID\t\t\t{self.user.id}\n"
			+ f"Discord Version\t\t{discord.__version__}\n"
			+ f"Time\t\t\t{self.uptime.strftime('%F %T')}"
		)

	async def close(self) -> None:
		"""
		Cleanup before the bot exits.
		"""
		await self.session.close()
		for extension in EXTENSIONS:
			try:
				self.unload_extension(extension)
			except Exception as e:
				print(e, file=stderr)

		await super().close()

	def run(self) -> None:
		"""
		Run the bot.
		"""
		super().run(self.token, reconnect=True)

	async def on_message(self, message: Message) -> None:
		"""
		Allow for command chaining using `&&`
		"""
		if message.author.bot:
			return

		commands = message.content.split(" && ")
		for command in commands:
			message.content = command
			await self.invoke(await self.get_context(message))


def get_prefix(bot: SRBpp, message: Message) -> list[str]:
	"""
	Gets the list of prefixes that can be used to call the bot, including pinging the bot.
	"""
	PREFIXES: tuple[str, ...] = ("+", ";")
	return commands.when_mentioned_or(*PREFIXES)(bot, message)
