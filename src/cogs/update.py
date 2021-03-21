from subprocess import CompletedProcess, run
from sys import stderr

import discord
from discord.ext import commands

from bot import SRBpp

Context = commands.context.Context


class Update(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	async def isbotmaster(ctx: Context) -> bool:
		"""
		Check if the caller of the command is a 'botmaster' or not. To
		learn how to configure who is and isn't a botmaster, see the
		man page `man/srbpp.json.5`.
		"""
		if ctx.author.id in ctx.bot.config["botmasters"]:
			return True
		else:
			await ctx.send("You do not have permission to execute this command.")
			return False

	@commands.check(isbotmaster)
	@commands.command(name="pull")
	async def pull(_, ctx: Context) -> None:
		"""
		Pull any changes from the GitHub repository.
		"""
		RET: CompletedProcess = run(("git", "pull"), capture_output=True, text=True)

		if RET.returncode == 1:
			await ctx.send(RET.stderr)
			return

		embed = discord.Embed(title="Git Pull", description=RET.stdout)
		await ctx.send(embed=embed)

	@commands.check(isbotmaster)
	@commands.command(name="reload")
	async def reload(self, ctx: Context, EXT: str) -> None:
		"""
		Reloads an extension.
		"""
		try:
			self.bot.reload_extension(f"cogs.{EXT}")
			await ctx.send(f"The extension {EXT} was reloaded.")
		except commands.ExtensionNotFound:
			await ctx.send(f"The extension {EXT} doesn't exist.")
		except commands.ExtensionNotLoaded:
			await ctx.send(f"The extension {EXT} is not loaded.")
		except commands.NoEntryPointError:
			await ctx.send(
				f"The extension {EXT} doesn't have an entry point. (Try adding the setup function)"
			)
		except commands.ExtensionFailed as e:
			await ctx.send(
				f"Some unknown error happened while trying to reload extension {EXT}."
			)
			print(e, file=stderr)

	@commands.check(isbotmaster)
	@commands.command(name="load")
	async def load(self, ctx: Context, EXT: str) -> None:
		"""
		Loads an extension.
		"""
		try:
			self.bot.load_extension(f"cogs.{EXT}")
			await ctx.send(f"The extension {EXT} was loaded.")
		except commands.ExtensionNotFound:
			await ctx.send(f"The extension {EXT} doesn't exist.")
		except commands.ExtensionAlreadyLoaded:
			await ctx.send(f"The extension {EXT} is already loaded.")
		except commands.NoEntryPointError:
			await ctx.send(
				f"The extension {EXT} doesn't have an entry point. (Try adding the setup function)"
			)
		except commands.ExtensionFailed as e:
			await ctx.send(
				f"Some unknown error happened while trying to reload extension {EXT}."
			)
			print(e, file=stderr)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Update(bot))
