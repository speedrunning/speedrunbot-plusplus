from subprocess import CompletedProcess

import discord
from discord.ext import commands
from discord.ext.commands.context import Context

from bot import SRBpp

TITLE: str
DESC: str
PREFIX: str = "srcom/bin"


class Src(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	@commands.command(name="categories", aliases=("cats",))
	async def categories(self, ctx: Context, GAME: str = None) -> None:
		"""
		Get a list of all of a games categories.
		"""
		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/categories", GAME)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		TITLE, DESC = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=DESC)
		await ctx.send(embed=embed)

	@commands.command(name="categoriesplayed", aliases=("catsplayed",))
	async def categoriesplayed(self, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the number of unique categories a player has submit runs to.
		"""
		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/categoriesplayed", PLAYER)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(
			title=f"Categories Played: {PLAYER}", description=RET.stdout
		)
		await ctx.send(embed=embed)

	@commands.command(name="games")
	async def games(self, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the number of unique games a player has submit runs to.
		"""
		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/games", PLAYER)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(title=f"Games Played: {PLAYER}", description=RET.stdout)
		await ctx.send(embed=embed)

	@commands.command(name="leaderboard", aliases=("lb",))
	async def leaderboard(
		self, ctx: Context, GAME: str = None, CAT: str = None, SUBCAT: str = None
	) -> None:
		"""
		Get the top 10 runs for a game, with an optional category and subcategory.
		"""
		RET: CompletedProcess = self.bot.execv(
			f"{PREFIX}/leaderboard", GAME, CAT, SUBCAT
		)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		TITLE, DESC = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=DESC)
		await ctx.send(embed=embed)

	@commands.command(name="modcount", aliases=("mc",))
	async def modcount(self, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the number of games and series a player moderates.
		"""
		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/modcount", PLAYER)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(
			title=f"Leaderboards Moderated: {PLAYER}", description=RET.stdout
		)
		await ctx.send(embed=embed)

	@commands.command(name="runqueue", aliases=("queue",))
	async def runqueue(self, ctx: Context, GAME: str = None) -> None:
		"""
		Get the number of runs awaiting verification for a given game
		"""
		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/runqueue", GAME)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		TITLE, DESC = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=DESC)
		await ctx.send(embed=embed)

	@commands.command(name="runs")
	async def runs(self, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the amount of runs a player has submit.
		"""
		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/runs", PLAYER)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(title=f"Run Count: {PLAYER}", description=RET.stdout)
		await ctx.send(embed=embed)

	@commands.command(name="verified")
	async def verified(self, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the amount of runs a player has verified or rejected.
		"""
		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/verified", PLAYER)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(
			title=f"Runs verified: {PLAYER}", description=RET.stdout
		)
		await ctx.send(embed=embed)

	@commands.command(name="worldrecord", aliases=("wr",))
	async def worldrecord(
		self, ctx: Context, GAME: str = None, CAT: str = None, SUBCAT: str = None
	) -> None:
		"""
		Get the world record for a game, with an optional category and subcategory.
		"""
		RET: CompletedProcess = self.bot.execv(
			f"{PREFIX}/worldrecord", GAME, CAT, SUBCAT
		)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		TITLE, DESC = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=DESC)
		await ctx.send(embed=embed)

	@commands.command(name="worldrecords", aliases=("wrs",))
	async def worldrecords(self, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the number of world records a player currently holds.
		"""
		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/worldrecords", PLAYER)
		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(
			title=f"World Record Count: {PLAYER}", description=RET.stdout
		)
		await ctx.send(embed=embed)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Src(bot))
