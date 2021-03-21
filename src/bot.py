import json
import os
from datetime import datetime
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import Iterable

import discord
from discord.ext import commands
from discord.message import Message

PREFIX: Path = Path(__file__).parent
DATA: str = f"{PREFIX}/../data"
EXTENSIONS: Iterable[str] = (
	f"cogs.{f[:-3]}" for f in os.listdir(f"{PREFIX}/cogs") if f.endswith(".py")
)


class SRBpp(commands.Bot):
	def __init__(self) -> None:
		super().__init__(
			command_prefix=get_prefix,
			case_insensitive=True,
			allowed_mentions=discord.AllowedMentions(
				everyone=False, users=True, roles=False
			),
		)

		for extension in EXTENSIONS:
			try:
				self.load_extension(extension)
			except Exception as e:
				print(e)

		with open(f"{DATA}/srbpp.json", "r") as f:
			self.config = json.load(f)

	def execv(_, PROG: str, *ARGS: tuple[str, ...]) -> CompletedProcess:
		"""
		Run a program as a subprocess and return its output + exit code.
		"""
		return run(
			(f"{PREFIX}/{PROG}",) + tuple(filter(lambda x: x, ARGS)),
			capture_output=True,
			text=True,
		)

	async def on_ready(self) -> None:
		"""
		Code to run when the bot starts up.
		"""
		self.uptime: datetime = datetime.utcnow()
		GAME: discord.Game = discord.Game("!help / ;help")
		await self.change_presence(activity=GAME)

	async def close(self) -> None:
		"""
		Cleanup before the bot exits.
		"""
		for extension in EXTENSIONS:
			try:
				self.unload_extension(extension)
			except Exception as e:
				print(e)

		await super().close()

	def run(self) -> None:
		"""
		Run the bot.
		"""
		super().run(self.config["token"], reconnect=True)


def get_prefix(bot: SRBpp, message: Message) -> list[str]:
	"""
	Gets the list of prefixes that can be used to call the bot, including
	pinging the bot.
	"""
	PREFIXES: tuple[str, ...] = ("!", ";", "+")
	return commands.when_mentioned_or(*PREFIXES)(bot, message)
