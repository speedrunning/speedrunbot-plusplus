from typing import Literal, Optional, Union

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.cooldowns import Cooldown

from bot import SRBpp, run_and_output

PREFIX: Literal[str] = "srcom/bin"
RATE: Literal[int] = 5


class Src(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot = bot
		self._cd = commands.CooldownMapping.from_cooldown(RATE, 60, commands.BucketType.user)

	async def cog_check(self, ctx: Context) -> True:
		"""
		Fuck you Khalooody.
		"""
		if ctx.invoked_with == "help":
			return True

		bucket = self._cd.get_bucket(ctx.message)
		retry_after = bucket.update_rate_limit()
		if retry_after:
			raise commands.CommandOnCooldown(bucket, retry_after)

		return True

	@commands.command(name="categories", aliases=("cats",))
	async def categories(_, ctx: Context, game: Optional[str] = None) -> None:
		"""
		Get a list of all of a games categories.
		"""
		await run_and_output(ctx, f"{PREFIX}/categories", game)

	@commands.command(name="categoriesplayed", aliases=("catsplayed",))
	async def categoriesplayed(_, ctx: Context, player: Optional[str] = None) -> None:
		"""
		Get the number of unique categories a player has submit runs to.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/categoriesplayed",
			player,
			title=f"Categories Played: {player}",
		)

	@commands.command(name="games")
	async def games(_, ctx: Context, player: Optional[str] = None) -> None:
		"""
		Get the number of unique games a player has submit runs to.
		"""
		await run_and_output(ctx, f"{PREFIX}/games", player, title=f"Games Played: {player}")

	@commands.command(name="leaderboard", aliases=("lb",))
	async def leaderboard(
		_,
		ctx: Context,
		game: Optional[str] = None,
		category: Optional[str] = None,
		subcategory: Optional[str] = None,
	) -> None:
		"""
		Get the top 10 runs for a game, with an optional category and subcategory.
		"""
		await run_and_output(ctx, f"{PREFIX}/leaderboard", game, category, subcategory)

	@commands.command(name="modcount", aliases=("mc",))
	async def modcount(_, ctx: Context, player: Optional[str] = None) -> None:
		"""
		Get the number of games and series a player moderates.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/modcount",
			player,
			title=f"Leaderboards Moderated {player}",
		)

	@commands.command(name="runqueue", aliases=("queue",))
	async def runqueue(
		_,
		ctx: Context,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get the number of runs awaiting verification for a given game. Optionally, a second
		game can be given.
		"""
		await run_and_output(ctx, f"{PREFIX}/runqueue", game1, game2)

	@commands.command(name="runs")
	async def runs(
		_,
		ctx: Context,
		player: Optional[str] = None,
		game: Optional[str] = None,
	) -> None:
		"""
		Get the amount of runs a player has submit. Optionally a game can be specified.
		"""
		await run_and_output(ctx, f"{PREFIX}/runs", player, game)

	@commands.command(name="verified")
	async def verified(
		_,
		ctx: Context,
		player: Optional[str] = None,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get the amount of runs a player has verified or rejected. Optionally 1 or 2 games
		can be specified.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/verified",
			player,
			game1,
			game2,
			title=f"Runs Verified: {player}",
		)

	@commands.command(name="worldrecord", aliases=("wr",))
	async def worldrecord(
		_,
		ctx: Context,
		game: Optional[str] = None,
		category: Optional[str] = None,
		subcategory: Optional[str] = None,
	) -> None:
		"""
		Get the world record for a game, with an optional category and subcategory.
		"""
		await run_and_output(ctx, f"{PREFIX}/worldrecord", game, category, subcategory)

	@commands.command(name="worldrecords", aliases=("wrs",))
	async def worldrecords(
		_,
		ctx: Context,
		player: Optional[str] = None,
		game: Optional[str] = None,
	) -> None:
		"""
		Get the number of world records a player currently holds.
		"""
		await run_and_output(ctx, f"{PREFIX}/worldrecords", player, game)

	@commands.command(name="pending")
	async def pending(
		_,
		ctx: Context,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get all pending runs for a game. Optionally 2 games can be given.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/pending",
			game1,
			game2,
			title=f"Pending runs for {game1 if not game2 else ' and '.join((game1, game2))}",
		)

	@commands.command(name="verifierleaderboard", aliases=("vlb",))
	async def verifierleaderboard(
		_,
		ctx: Context,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get a leaderboard of a games verifiers and how many runs each has examined.
		Optionally 2 games can be specified.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/verifierleaderboard",
			game1,
			game2,
			title=f"Verifier Leaderboard for {game1 if not game2 else ' and '.join((game1, game2))}",
		)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Src(bot))
