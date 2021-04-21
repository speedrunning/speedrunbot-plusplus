import asyncio
import os
import shlex
from datetime import datetime
from pathlib import Path
from sys import stderr
from typing import Iterable, Union

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message

RET: int
STDOUT: bytes
STDERR: bytes

TITLE: str
DESC: str

PREFIX: Path = Path(__file__).parent
ROOT_DIR: str = f"{PREFIX}/.."
EXTENSIONS: Iterable[str] = (
	f"cogs.{f[:-3]}" for f in os.listdir(f"{PREFIX}/cogs") if f.endswith(".py")
)


def divide_chunks(l: list, n: int):
	# looping till length l
	for i in range(0, len(l), n):
		yield l[i : i + n]


async def execv(PROG: str, *ARGV: tuple[str, ...]) -> tuple[int, bytes, bytes]:
	"""
	Run a program called PROG with the command line arguments ARGV. This returns
	a tuple containing the processes returncode, as well as the encoded stdout and
	stderr.
	"""
	# This is like `shlex.join()`, but it gets rid of any `None` values.
	ARGS: str = " ".join(
		shlex.quote(arg) for arg in tuple(filter(lambda x: x, ARGV))
	)

	RET = await asyncio.create_subprocess_shell(
		f"{PREFIX}/{PROG} {ARGS}",
		stdout=asyncio.subprocess.PIPE,
		stderr=asyncio.subprocess.PIPE,
	)
	STDOUT, STDERR = await RET.communicate()
	return (RET.returncode, STDOUT, STDERR)


async def run_and_output(
	ctx: Context,
	PROG: str,
	*ARGV: tuple[str, ...],
	TITLE: Union[str, None] = None,
) -> None:
	"""
	Run a program called PROG with the command line arguments ARGV as a
	subprocess and return its output + exit code. If TITLE is supplied, it
	will be used as the title of the embed that is sent to discord. If TITLE
	is not supplied, then the first line of output from PROG will be used.
	"""
	async with ctx.typing():
		RETCODE, STDOUT, STDERR = await execv(PROG, *ARGV)
		if RETCODE != 0:
			await ctx.send(STDERR.decode())
			return

		TITLE, DESC = (
			STDOUT.decode().split("\n", 1)
			if not TITLE
			else [TITLE, STDOUT.decode()]
		)
		if len(DESC) > 2000:
			LINES = list(divide_chunks(DESC.split("\n"), 15))
			LINES_LENGTH: int = len(LINES)
			try:
				await ctx.reply(
					"The contents of this message are too long and as such they will be sent in DMs"
				)
				async with ctx.author.typing():
					for line in range(LINES_LENGTH):
						await ctx.author.send(
							embed=discord.Embed(
								title=f"{TITLE} Page: {line + 1}/{LINES_LENGTH}",
								description="\n".join(LINES[line]),
							)
						)
			except discord.Forbidden:
				await ctx.reply(
					"You have blocked the bot and the message is too long to be sent in this channel. Please unblock me and try again. "
				)
		else:
			EMBED = discord.Embed(title=TITLE, description=DESC)
			await ctx.reply(embed=EMBED)


class SRBpp(commands.Bot):
	def __init__(self) -> None:
		super().__init__(
			allowed_mentions=discord.AllowedMentions(
				everyone=False, users=False, roles=False
			),
			case_insensitive=True,
			command_prefix=get_prefix,
			intents=discord.Intents(messages=True, guilds=True),
			help_command=commands.MinimalHelpCommand(dm_help=True),
		)

		for extension in EXTENSIONS:
			try:
				self.load_extension(extension)
			except Exception as e:
				print(e, file=stderr)

		with open(f"{ROOT_DIR}/token", "r") as f:
			self.token = f.read().strip()

	async def on_ready(self) -> None:
		"""
		Code to run when the bot starts up.
		"""
		self.uptime: datetime = datetime.utcnow()
		GAME: discord.Game = discord.Game("+help / ;help")
		await self.change_presence(activity=GAME)

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

		COMMANDS: list[str] = message.content.split(" && ")
		for command in COMMANDS:
			message.content = command
			await self.invoke(await self.get_context(message))


def get_prefix(bot: SRBpp, message: Message) -> list[str]:
	"""
	Gets the list of prefixes that can be used to call the bot, including
	pinging the bot.
	"""
	PREFIXES: tuple[str, ...] = ("+", ";")
	return commands.when_mentioned_or(*PREFIXES)(bot, message)
