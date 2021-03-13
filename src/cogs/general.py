from discord.ext import commands

from bot import SRBpp

Context = commands.context.Context


class General(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	@commands.command(name="source")
	async def source(_, ctx: Context) -> None:
		SRC: str = "https://www.github.com/Mango0x45/speedrunbot-plusplus"
		await ctx.send(SRC)

	@commands.command(name="ping")
	async def ping(self, ctx: Context) -> None:
		LATENCY: int = round(self.bot.latency * 1000)
		await ctx.send(f"Pong! {LATENCY}ms")

	@commands.command(name="invite")
	async def invite(_, ctx: Context) -> None:
		INV: str = (
			"https://discord.com/oauth2/authorize?client_id=644879546650198016&scope=bot"
		)
		await ctx.send(INV)


def setup(bot: SRBpp) -> None:
	bot.add_cog(General(bot))
