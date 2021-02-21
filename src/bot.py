import datetime
import json
import subprocess

import discord
from discord.ext import commands

DATA = "../data"
EXTENSIONS = ("cogs.general", "cogs.src")


def get_prefix(bot, message):
    prefixes = ("!", ";", "+")
    return commands.when_mentioned_or(*prefixes)(bot, message)


class SRBpp(commands.Bot):
    def __init__(self):
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

    def run_prog(self, prog, args=None):
        ret = subprocess.check_output(f"{prog} {args}", shell=True)
        return ret.decode("utf-8").replace("\\\n", "").strip()

    async def on_ready(self):
        self.uptime = datetime.datetime.utcnow()
        game = discord.Game("!help / ;help")
        await self.change_presence(activity=game)

    async def close(self):
        for extension in EXTENSIONS:
            try:
                self.unload_extension(extension)
            except Exception:
                pass

        await super().close()

    def run(self):
        super().run(self.config["token"], reconnect=True)
