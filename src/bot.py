import json
import os
from datetime import datetime
from pathlib import Path
from subprocess import CompletedProcess, run

import discord
from discord.ext import commands

PREFIX: Path = Path(__file__).parent
DATA: str = f"{PREFIX}/../data"
EXTENSIONS: tuple[str] = tuple(
    f"cogs.{f[:-3]}" for f in os.listdir(f"{PREFIX}/cogs") if f.endswith(".py")
)


def get_prefix(bot, message):
    prefixes = ("!", ";", "+")
    return commands.when_mentioned_or(*prefixes)(bot, message)


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
            self.load_extension(extension)

        with open(f"{DATA}/config.json", "r") as f:
            self.config = json.load(f)

    def execv(_, PROG: str, *ARGS: tuple[str]) -> CompletedProcess:
        """
        Run a program as a subprocess and return its output + return code.
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
        self.uptime = datetime.utcnow()
        game: discord.Game = discord.Game("!help / ;help")
        await self.change_presence(activity=game)

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
