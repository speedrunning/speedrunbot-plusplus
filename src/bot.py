import datetime
import json
from pathlib import Path
from subprocess import CompletedProcess, run

import discord
from discord.ext import commands

DATA: str = f"{Path(__file__).parent}/../data"
EXTENSIONS: tuple[str] = ("cogs.general", "cogs.src")


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
            config = self.config

    def execv(self, PROG: str, *ARGS: tuple[str]) -> CompletedProcess:
        """
        Run a program as a subprocess and return its output + return code

        >>> SRBpp.execv("echo", "-n", "testy test")
        CompletedProcess(args=('echo', '-n', 'testy test'), returncode=0, stdout='testy test', stderr='')
        >>> SRBpp.execv("echo", "yet", "another", None, "testy test")
        CompletedProcess(args=('echo', 'yet', 'another', 'testy test'), returncode=0, stdout='yet another testy test\\n', stderr='')
        """
        return run(
            (PROG,) + tuple(filter(lambda x: x, ARGS)),
            capture_output=True,
            text=True,
        )

    async def on_ready(self) -> None:
        self.uptime = datetime.datetime.utcnow()
        game = discord.Game("!help / ;help")
        await self.change_presence(activity=game)

    async def close(self) -> None:
        for extension in EXTENSIONS:
            try:
                self.unload_extension(extension)
            except Exception:
                pass

        await super().close()

    def run(self) -> None:
        """Run the bot."""
        super().run(self.config["token"], reconnect=True)
