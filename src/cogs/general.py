from discord.ext import commands
from discord.ext.commands.context import Context

from bot import SRBpp


class General(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	@commands.command(name="source")
	async def source(_, ctx: Context) -> None:
		"""
		Link the bots GitHub repository.
		"""
		SRC: str = "https://www.github.com/Mango0x45/speedrunbot-plusplus"
		await ctx.send(SRC)

	@commands.command(name="ping")
	async def ping(self, ctx: Context) -> None:
		"""
		Ping the bot, because why not?
		"""
		LATENCY: int = round(self.bot.latency * 1000)
		await ctx.send(f"Pong! {LATENCY}ms")

	@commands.command(name="invite")
	async def invite(_, ctx: Context) -> None:
		"""
		Get the bots discord invite link.
		"""
		INV: str = (
			"https://discord.com/oauth2/authorize?client_id=644879546650198016&scope=bot"
		)
		await ctx.send(INV)


def setup(bot: SRBpp) -> None:
	bot.add_cog(General(bot))
