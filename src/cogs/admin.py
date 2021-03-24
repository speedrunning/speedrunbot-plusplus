from os import listdir, path
from subprocess import CompletedProcess, run
from sys import stderr

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandError

from bot import SRBpp


class Admin(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	async def isbotmaster(ctx: Context) -> bool:
		"""
		Check if the caller of the command is a 'botmaster' or not. To
		learn how to configure who is and isn't a botmaster, see the
		docs at `data/README.md`.
		"""
		if ctx.author.id in ctx.bot.config["botmasters"]:
			return True
		else:
			return False

	@commands.Cog.listener()
	async def on_command_error(_, ctx: Context, err: CommandError) -> None:
		"""
		A simple error handler to avoid spamming my console with errors
		I do not care about.
		"""
		if type(err) == commands.CheckFailure:
			await ctx.send("You do not have permission to execute this command.")
		elif type(err) == commands.errors.CommandNotFound:
			COMMAND: str = err.args[0].split('"')[1]
			await ctx.send(f"Command '{COMMAND}' does not exist.")
		else:
			# TODO: Make it DM me the error maybe?
			print(type(err), file=stderr)
			print(err, file=stderr)

	@commands.check(isbotmaster)
	@commands.command(name="make")
	async def make(_, ctx: Context) -> None:
		"""
		Run the bots Makefiles to update all the code.
		"""
		MAKE_EXCLUDES: tuple[str, ...] = ("__pycache__", "cogs")
		PATH: str = path.dirname(__file__)
		FILES: list[str] = listdir(f"{PATH}/../")

		output: str = ""
		for file in FILES:
			fpath: str = f"{PATH}/../{file}"
			if path.isdir(fpath) and file not in MAKE_EXCLUDES:
				RET: CompletedProcess = run(
					("make", "-C", fpath), capture_output=True, text=True
				)
				output += RET.stdout

		# If you compile a lot of stuff, you end up with lots of output.
		while len(output) > 0:
			await ctx.send(f"```{output[0:2000 - 6]}```")
			output = output[2000 - 6 :]

	@commands.check(isbotmaster)
	@commands.command(name="pull")
	async def pull(_, ctx: Context) -> None:
		"""
		Pull any changes from the GitHub repository.
		"""
		RET: CompletedProcess = run(("git", "pull"), capture_output=True, text=True)

		if RET.returncode != 0:
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

	@commands.check(isbotmaster)
	@commands.command(name="unload")
	async def unload(self, ctx: Context, EXT: str) -> None:
		"""
		Unloads an extension.
		"""
		try:
			self.bot.unload_extension(f"cogs.{EXT}")
			await ctx.send(f"The extension {EXT} was unloaded.")
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
	bot.add_cog(Admin(bot))
