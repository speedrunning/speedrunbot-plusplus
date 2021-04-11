from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.cooldowns import Cooldown

from bot import SRBpp, run_and_output

PREFIX: str = "halo/bin"
RATE: int = 5


class Halo(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot
		self._cd = commands.CooldownMapping.from_cooldown(
			RATE, 60, commands.BucketType.user
		)

	@commands.group(name="halo", invoke_without_command=True)
	async def halo(self, ctx):
		await ctx.send_help(self)

	@halo.command(name="recent", aliases=("cats",))
	async def recent(_, ctx: Context, COUNT: int = None) -> None:
		"""
		Get a list of recent runs.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/recent",
			str(COUNT) if COUNT else None,
			TITLE="Recent World Records",
		)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Halo(bot))
