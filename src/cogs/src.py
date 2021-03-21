from subprocess import CompletedProcess

import discord
from discord.ext import commands

from bot import SRBpp

Context = commands.context.Context
PREFIX: str = "srcom/bin"


class Src(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	@commands.command(name="categories", aliases=("cats",))
	async def categories(self, ctx: Context, GAME: str = None) -> None:
		if not GAME:
			await ctx.send(
				"Usage: `!categories [GAME]`\n" + "Example: `!categories mcbe`"
			)
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/categories", GAME)

		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		TITLE, CATS = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=CATS)
		await ctx.send(embed=embed)

	@commands.command(name="categoriesplayed", aliases=("catsplayed",))
	async def categoriesplayed(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send(
				"Usage: `!categoriesplayed [PLAYER NAME]`\n"
				+ "Example: `!categoriesplayed AnInternetTroll`"
			)
			return

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
		if not PLAYER:
			await ctx.send(
				"Usage: `!games [PLAYER NAME]`\n" + "Example: `!games AnInternetTroll`"
			)
			return

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
		if not GAME:
			await ctx.send(
				"Usage: `!leaderboard [GAME] [CATEGORY (Optional)] [SUBCATEGORY (Optional)]`\n"
				+ 'Example: `!leaderboard mkw "Nitro Tracks"`'
			)
			return

		RET: CompletedProcess = self.bot.execv(
			f"{PREFIX}/leaderboard", GAME, CAT, SUBCAT
		)

		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		TITLE, LB = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=LB)
		await ctx.send(embed=embed)

	@commands.command(name="modcount", aliases=("mc",))
	async def modcount(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send(
				"Usage: `!modcount [PLAYER NAME]`\n"
				+ "Example: `!modcount AnInternetTroll`"
			)
			return

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
		if not GAME:
			await ctx.send("Usage: `!runqueue [GAME]`\n" + "Example: `!runqueue mkw`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/runqueue", GAME)

		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(
			title=f"Runs Awaiting Verification: {GAME}", description=RET.stdout
		)
		await ctx.send(embed=embed)

	@commands.command(name="runs")
	async def runs(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send(
				"Usage: `!runs [PLAYER NAME]`\n" + "Example: `!runs AnInternetTroll`"
			)
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/runs", PLAYER)

		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(title=f"Run Count: {PLAYER}", description=RET.stdout)
		await ctx.send(embed=embed)

	@commands.command(name="verified")
	async def verified(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send(
				"Usage: `!verified [PLAYER NAME]`\n"
				+ "Example: `!verified AnInternetTroll`"
			)
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/verified", PLAYER)

		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(title="Runs verified: {PLAYER}", description=RET.stdout)
		await ctx.send(embed=embed)

	@commands.command(name="worldrecord", aliases=("wr",))
	async def worldrecord(
		self, ctx: Context, GAME: str = None, CAT: str = None, SUBCAT: str = None
	) -> None:
		if not GAME:
			await ctx.send(
				"Usage: `!worldrecord [GAME] [CATEGORY (Optional)] [SUBCATEGORY (Optional)]`\n"
				+ 'Example: `!worldrecord mkw "Nitro Tracks"`'
			)
			return

		RET: CompletedProcess = self.bot.execv(
			f"{PREFIX}/worldrecord", GAME, CAT, SUBCAT
		)

		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		TITLE, WR = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=WR)
		await ctx.send(embed=embed)

	@commands.command(name="worldrecords", aliases=("wrs",))
	async def worldrecords(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send(
				"Usage: `!worldrecords [PLAYER NAME]`\n"
				+ "Example: `!worldrecords AnInternetTroll`"
			)
			return

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
