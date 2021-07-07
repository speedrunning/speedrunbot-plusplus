from typing import Literal, Optional, Union

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.cooldowns import Cooldown
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

from bot import SRBpp, run_and_output

PREFIX = "srcom/bin"
RATE = 5

class Src(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot = bot
		self._cd = commands.CooldownMapping.from_cooldown(RATE, 60, commands.BucketType.user)

	def cog_check(self, ctx: Union[Context, SlashContext]) -> Literal[True]:
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

	async def categories(_, ctx: Union[Context, SlashContext], game: Optional[str] = None) -> None:
		"""
		Get a list of all of a games categories.
		"""
		await run_and_output(ctx, f"{PREFIX}/categories", game)

	async def categoriesplayed(
		_, ctx: Union[Context, SlashContext], player: Optional[str] = None
	) -> None:
		"""
		Get the number of unique categories a player has submit runs to.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/categoriesplayed",
			player,
			title=f"Categories Played: {player}",
		)

	async def games(_, ctx: SlashContext, player: Optional[str] = None) -> None:
		"""
		Get the number of unique games a player has submit runs to.
		"""
		await run_and_output(ctx, f"{PREFIX}/games", player, title=f"Games Played: {player}")

	async def leaderboard(
		_,
		ctx: SlashContext,
		game: Optional[str] = None,
		category: Optional[str] = None,
		subcategory: Optional[str] = None,
	) -> None:
		"""
		Get the top 10 runs for a game, with an optional category and subcategory.
		"""
		await run_and_output(ctx, f"{PREFIX}/leaderboard", game, category, subcategory)

	async def modcount(_, ctx: Union[Context, SlashContext], player: Optional[str] = None) -> None:
		"""
		Get the number of games and series a player moderates.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/modcount",
			player,
			title=f"Leaderboards Moderated: {player}",
		)

	async def posts(_, ctx: Union[Context, SlashContext], player: Optional[str] = None) -> None:
		"""
		Get the number of forum posts a user has made.
		"""
		await run_and_output(ctx, f"{PREFIX}/posts", player, title=f"Forum Posts: {player}")

	async def verified(
		_,
		ctx: Union[Context, SlashContext],
		player: Optional[str] = None,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get the amount of runs a player has verified or rejected. Optionally 1 or 2 games can be specified.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/verified",
			player,
			game1,
			game2,
			title=f"Runs Verified: {player}",
		)

	async def worldrecords(
		_,
		ctx: Union[Context, SlashContext],
		player: Optional[str] = None,
		game: Optional[str] = None,
	) -> None:
		"""
		Get the number of world records a player currently holds.
		"""
		await run_and_output(ctx, f"{PREFIX}/worldrecords", player, game)

	async def verifierleaderboard(
		_,
		ctx: Union[Context, SlashContext],
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

	async def pending(
		_,
		ctx: Union[Context, SlashContext],
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

	async def worldrecord(
		_,
		ctx: Union[Context, SlashContext],
		game: Optional[str] = None,
		category: Optional[str] = None,
		subcategory: Optional[str] = None,
	) -> None:
		"""
		Get the world record for a game, with an optional category and subcategory.
		"""
		await run_and_output(ctx, f"{PREFIX}/worldrecord", game, category, subcategory)

	async def podiums(
		_,
		ctx: Union[Context, SlashContext],
		player: Optional[str] = None,
	) -> None:
		"""
		Get the number of top 3 runs a player has.
		"""
		await run_and_output(ctx, f"{PREFIX}/podiums", player)

	@cog_ext.cog_slash(
		name="categories",
		description="Get a list of all of a games categories.",
		options=[
			create_option(
				name="game", description="The abbreviation of a game.", option_type=3, required=True
			),
		],
	)
	async def categories_slash(self, ctx: SlashContext, game: str) -> None:
		await self.categories(ctx, game)

	@commands.command(name="categories", aliases=("cats",))
	async def categories_bot(self, ctx: Context, game: Optional[str] = None) -> None:
		"""
		Get a list of all of a games categories.
		"""
		await self.categories(ctx, game)

	@cog_ext.cog_slash(
		name="categoriesplayed",
		description="Get the number of unique categories a player has submit runs to.",
		options=[
			create_option(
				name="player", description="The username of a player.", option_type=3, required=True
			),
		],
	)
	async def categoriesplayed_slash(self, ctx: SlashContext, player: str) -> None:
		await self.categoriesplayed(ctx, player)

	@commands.command(name="categoriesplayed", aliases=("catsplayed",))
	async def categoriesplayed_bot(self, ctx: Context, player: Optional[str] = None) -> None:
		"""
		Get the number of unique categories a player has submit runs to.
		"""
		await self.categoriesplayed(ctx, player)

	@cog_ext.cog_slash(
		name="games",
		description="Get the number of unique games a player has submit runs to.",
		options=[
			create_option(
				name="player", description="The username of a player.", option_type=3, required=True
			),
		],
	)
	async def games_slash(self, ctx: SlashContext, player: str) -> None:
		await self.games(ctx, player)

	@commands.command(name="games")
	async def games_bot(self, ctx: Context, player: Optional[str] = None) -> None:
		"""
		Get the number of unique games a player has submit runs to.
		"""
		await self.games(ctx, player)

	@cog_ext.cog_slash(
		name="leaderboard",
		description="Get the top 10 runs for a game, with an optional category and subcategory.",
		options=[
			create_option(
				name="game", description="The abbreviation of a game.", option_type=3, required=True
			),
			create_option(
				name="category", description="A category.", option_type=3, required=False
			),
			create_option(
				name="subcategory",
				description="A subcategory or variable.",
				option_type=3,
				required=False,
			),
		],
	)
	async def leaderboard_slash(
		self,
		ctx: SlashContext,
		game: str,
		category: Optional[str] = None,
		subcategory: Optional[str] = None,
	) -> None:
		await self.leaderboard(ctx, game, category, subcategory)

	@commands.command(name="leaderboard", aliases=("lb",))
	async def leaderboard_bot(
		self,
		ctx: Context,
		game: Optional[str] = None,
		category: Optional[str] = None,
		subcategory: Optional[str] = None,
	) -> None:
		"""
		Get the top 10 runs for a game, with an optional category and subcategory.
		"""
		await self.leaderboard(ctx, game, category, subcategory)

	@cog_ext.cog_slash(
		name="modcount",
		description="Get the number of games and series a player moderates.",
		options=[
			create_option(
				name="player", description="The username of a player.", option_type=3, required=True
			),
		],
	)
	async def modcount_slash(self, ctx: SlashContext, player: str) -> None:
		await self.modcount(ctx, player)

	@commands.command(name="modcount", aliases=("mc",))
	async def modcount_bot(self, ctx: Context, player: Optional[str] = None) -> None:
		"""
		Get the number of runs awaiting verification for a given game. Optionally, a second game can be given.
		"""
		await self.modcount(ctx, player)

	@cog_ext.cog_slash(
		name="posts",
		description="Get the number of forum posts a user has made.",
		options=[
			create_option(
				name="player", description="The username of a player.", option_type=3, required=True
			)
		]
	)
	async def posts_slash(self, ctx: SlashContext, player: str) -> None:
		await self.posts(ctx, player)

	@commands.command(name="posts", aliases=("p",))
	async def posts_bot(self, ctx: Context, player: Optional[str] = None) -> None:
		"""
		Get the number of forum posts a user has made.
		"""
		await self.posts(ctx, player)

	async def runqueue(
		_,
		ctx: Union[Context, SlashContext],
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get the number of runs awaiting verification for a given game. Optionally, a second
		game can be given.
		"""
		await run_and_output(ctx, f"{PREFIX}/runqueue", game1, game2)

	@cog_ext.cog_slash(
		name="runqueue",
		description="Get the number of runs awaiting verification for a given game.",
		options=[
			create_option(
				name="game1",
				description="The abbreviation of a game.",
				option_type=3,
				required=True,
			),
			create_option(
				name="game2",
				description="The abbreviation of a game.",
				option_type=3,
				required=False,
			),
		],
	)
	async def runqueue_slash(
		self, ctx: SlashContext, game1: str, game2: Optional[str] = None
	) -> None:
		await self.runqueue(ctx, game1, game2)

	@commands.command(name="runqueue", aliases=("queue",))
	async def runqueue_bot(
		self, ctx: Context, game1: Optional[str] = None, game2: Optional[str] = None
	) -> None:
		"""
		Get the number of runs awaiting verification for a given game. Optionally, a second
		game can be given.
		"""
		await self.runqueue(ctx, game1, game2)

	async def runs(
		_,
		ctx: Union[Context, SlashContext],
		player: Optional[str] = None,
		game: Optional[str] = None,
	) -> None:
		"""
		Get the amount of runs a player has submit. Optionally a game can be specified.
		"""
		await run_and_output(ctx, f"{PREFIX}/runs", player, game)

	@cog_ext.cog_slash(
		name="runs",
		description="Get the amount of runs a player has submit.",
		options=[
			create_option(
				name="player", description="The username of a player.", option_type=3, required=True
			),
			create_option(
				name="game",
				description="The abbreviation of a game.",
				option_type=3,
				required=False,
			),
		],
	)
	async def runs_slash(self, ctx: SlashContext, player: str, game: Optional[str] = None) -> None:
		await self.runs(ctx, player, game)

	@commands.command(name="runs")
	async def runs_bot(
		self, ctx: Context, player: Optional[str] = None, game: Optional[str] = None
	) -> None:
		"""
		Get the amount of runs a player has submit. Optionally a game can be specified.
		"""
		await self.runs(ctx, player, game)

	@cog_ext.cog_slash(
		name="verified",
		description="Get the amount of runs a player has verified or rejected.",
		options=[
			create_option(
				name="player", description="The username of a player.", option_type=3, required=True
			),
			create_option(
				name="game1",
				description="The abbreviation of a game.",
				option_type=3,
				required=False,
			),
			create_option(
				name="game2",
				description="The abbreviation of a game.",
				option_type=3,
				required=False,
			),
		],
	)
	async def verified_slash(
		self,
		ctx: SlashContext,
		player: str,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		await self.verified(ctx, player, game1, game2)

	@commands.command(name="verifierleaderboard", aliases=("vlb",))
	async def verifierleaderboard_bot(
		self,
		ctx: Context,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get a leaderboard of a games verifiers and how many runs each has examined.
		Optionally 2 games can be specified.
		"""
		await self.verifierleaderboard(ctx, game1, game2)

	@commands.command(name="verified")
	async def verified_bot(
		self,
		ctx: Context,
		player: Optional[str] = None,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get the amount of runs a player has verified or rejected. Optionally 1 or 2 games can be specified.
		"""
		await self.verified(ctx, player, game1, game2)

	@commands.command(name="worldrecord", aliases=("wr",))
	async def worldrecord_bot(
		self,
		ctx: Context,
		game: Optional[str] = None,
		category: Optional[str] = None,
		subcategory: Optional[str] = None,
	) -> None:
		"""
		Get the world record for a game, with an optional category and subcategory.
		"""
		await self.worldrecord(ctx, game, category, subcategory)

	@commands.command(name="worldrecords", aliases=("wrs",))
	async def worldrecords_bot(
		self,
		ctx: Context,
		player: Optional[str] = None,
		game: Optional[str] = None,
	) -> None:
		"""
		Get the number of world records a player currently holds.
		"""
		await self.worldrecords(ctx, player, game)

	@commands.command(name="pending")
	async def pending_bot(
		self,
		ctx: Context,
		game1: Optional[str] = None,
		game2: Optional[str] = None,
	) -> None:
		"""
		Get all pending runs for a game. Optionally 2 games can be given.
		"""
		await self.pending(ctx, game1, game2)

	@commands.command(name="podiums")
	async def podiums_bot(
		self,
		ctx: Context,
		player: Optional[str] = None,
	) -> None:
		"""
		Get the number of top 3 runs a player has.
		"""
		await self.podiums(ctx, player)

	@cog_ext.cog_slash(
		name="worldrecord",
		description="Get the world record for a game",
		options=[
			create_option(
				name="game", description="The abbreviation of a game.", option_type=3, required=True
			),
			create_option(
				name="category", description="A category.", option_type=3, required=False
			),
			create_option(
				name="subcategory",
				description="A subcategory or variable.",
				option_type=3,
				required=False,
			),
		],
	)
	async def worldrecord_slash(
		self,
		ctx: SlashContext,
		game: str,
		category: Optional[str] = None,
		subcategory: Optional[str] = None,
	) -> None:
		await self.worldrecord(ctx, game, category, subcategory)

	@cog_ext.cog_slash(
		name="worldrecords",
		description="Get the number of world records a player currently holds.",
		options=[
			create_option(
				name="player", description="The username of a player.", option_type=3, required=True
			),
			create_option(
				name="game",
				description="The abbreviation of a game.",
				option_type=3,
				required=False,
			),
		],
	)
	async def worldrecords_slash(
		self,
		ctx: SlashContext,
		player: str,
		game: Optional[str] = None,
	) -> None:
		await self.worldrecords(ctx, player, game)

	@cog_ext.cog_slash(
		name="pending",
		description="Get all pending runs for a game",
		options=[
			create_option(
				name="game1",
				description="The abbreviation of a game.",
				option_type=3,
				required=True,
			),
			create_option(
				name="game2",
				description="The abbreviation of a game.",
				option_type=3,
				required=False,
			),
		],
	)
	async def pending_slash(
		self,
		ctx: SlashContext,
		game1: str,
		game2: Optional[str] = None,
	) -> None:
		await self.pending(ctx, game1, game2)

	@cog_ext.cog_slash(
		name="verifierleaderboard",
		description="Get a leaderboard of a games verifiers and how many runs each has examined.",
		options=[
			create_option(
				name="game1",
				description="The abbreviation of a game.",
				option_type=3,
				required=True,
			),
			create_option(
				name="game2",
				description="The abbreviation of a game.",
				option_type=3,
				required=False,
			),
		],
	)
	async def verifierleaderboard_slash(
		self,
		ctx: SlashContext,
		game1: str,
		game2: Optional[str] = None,
	) -> None:
		await self.verifierleaderboard(ctx, game1, game2)

	@cog_ext.cog_slash(
		name="podiums",
		description="Get the number of top 3 runs a player has.",
		options=[
			create_option(
				name="player", description="The username of a player.", option_type=3, required=True
			),
		],
	)
	async def podiums_slash(
		self,
		ctx: SlashContext,
		player: str,
	) -> None:
		await self.podiums(ctx, player)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Src(bot))
