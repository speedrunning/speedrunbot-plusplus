from typing import Literal, Optional

from bot import SRBpp, run_and_output
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.cooldowns import Cooldown

PREFIX: Literal["halo/bin"] = "halo/bin"
RATE: Literal[5] = 5


class Halo(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot = bot
		self._cd = commands.CooldownMapping.from_cooldown(RATE, 60, commands.BucketType.user)

	@commands.group(name="halo", invoke_without_command=True)
	async def halo(_, ctx: Context) -> None:
		await ctx.send_help(ctx.command)

	@halo.command(name="recent", aliases=("cats",))
	async def recent(_, ctx: Context, count: Optional[str] = None) -> None:
		"""
		Get a list of recent runs.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/recent",
			count,
			title="Recent World Records",
		)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Halo(bot))
