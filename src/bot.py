import asyncio
import os
from datetime import datetime
from pathlib import Path
from sys import stderr
from typing import Iterable, Union

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message

TITLE: str
DESC: str

PREFIX: Path = Path(__file__).parent
ROOT_DIR: str = f"{PREFIX}/.."
EXTENSIONS: Iterable[str] = (
	f"cogs.{f[:-3]}" for f in os.listdir(f"{PREFIX}/cogs") if f.endswith(".py")
)

curr_procs: int = 0
MAX_PROCS: int = 15


async def execv(
	ctx: Context, PROG: str, *ARGV: tuple[str, ...], TITLE: Union[str, None] = None
) -> None:
	"""
	Run a program as a subprocess and return its output + exit code.
	"""
	global curr_procs, MAX_PROCS
	if curr_procs == MAX_PROCS:
		await ctx.send("Too many processes running. Try again in a moment.")
		return
	curr_procs += 1

	ARGS: str = " ".join(f'"{arg}"' for arg in tuple(filter(lambda x: x, ARGV)))
	RET = await asyncio.create_subprocess_shell(
		f"{PREFIX}/{PROG} {ARGS}",
		stdout=asyncio.subprocess.PIPE,
		stderr=asyncio.subprocess.PIPE,
	)
	STDOUT, STDERR = await RET.communicate()

	if RET.returncode != 0:
		await ctx.send(STDERR.decode())
		curr_procs -= 1
		return

	if TITLE is not None:
		embed = discord.Embed(title=TITLE, description=STDOUT.decode())
	else:
		TITLE, DESC = STDOUT.decode().split("\n", 1)
		embed = discord.Embed(title=TITLE, description=DESC)
	await ctx.send(embed=embed)

	curr_procs -= 1


class SRBpp(commands.Bot):
	def __init__(self) -> None:
		super().__init__(
			allowed_mentions=discord.AllowedMentions(
				everyone=False, users=False, roles=False
			),
			case_insensitive=True,
			command_prefix=get_prefix,
			intents=discord.Intents(messages=True, guilds=True),
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
		GAME: discord.Game = discord.Game("+help / !help")
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


def get_prefix(bot: SRBpp, message: Message) -> list[str]:
	"""
	Gets the list of prefixes that can be used to call the bot, including
	pinging the bot.
	"""
	PREFIXES: tuple[str, ...] = ("+", "!")
	return commands.when_mentioned_or(*PREFIXES)(bot, message)
