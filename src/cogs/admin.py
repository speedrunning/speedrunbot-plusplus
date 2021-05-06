import os
import sys
from math import trunc
from subprocess import CompletedProcess, run
from sys import stderr
from traceback import format_exception, print_exception
from typing import Literal

import discord
from bot import SRBpp, run_and_output
from cogs.src import RATE
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandError

PREFIX: Literal[str] = "admin/bin"


class Admin(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx: Context, err: CommandError) -> None:
		"""
		A simple error handler to avoid spamming my console with errors I do not care about.
		"""
		if type(err) in (
			commands.errors.CommandNotFound,
			commands.errors.CheckFailure,
		):
			pass
		elif type(err) == commands.errors.NotOwner:
			await ctx.send("You do not have permission to execute this command.")
		elif type(err) == commands.CommandOnCooldown:
			await ctx.send(
				f"You can only run {RATE} speedrun.com related commands per minute. Please wait {trunc(err.retry_after)} seconds."
			)
		elif type(err) == commands.errors.BadArgument:
			await ctx.send("Invalid argument, please check your input and try again.")
		else:  # TODO: Make it DM me the error maybe?
			print(f"{type(err)}: {err}", file=stderr)

			embed = discord.Embed(
				title=str(err),
				description=f"```py\n{''.join(format_exception(type(err), err, err.__traceback__))}```",
			)
			embed.add_field(name="Command invoked: ", value=ctx.invoked_with)
			await ctx.author.send(f"{type(err)}", embed=embed)

			# For debugging purposes uncomment the following line to enable detailed
			# error printing.
			# print_exception(type(err), err, err.__traceback__, file=stderr)

	@commands.is_owner()
	@commands.command(name="compile", aliases=("make", "comp"))
	async def compile(_, ctx: Context) -> None:
		"""
		Run the bots Makefiles to update all the code.
		"""
		await run_and_output(ctx, f"{PREFIX}/compile", title="Compile")

	@commands.is_owner()
	@commands.command(name="pull")
	async def pull(_, ctx: Context) -> None:
		"""
		Pull any changes from the GitHub repository.
		"""
		ret = run(("git", "pull"), capture_output=True, text=True)

		if ret.returncode != 0:
			await ctx.send(ret.stderr)
			return

		embed = discord.Embed(title="Git Pull", description=ret.stdout)
		await ctx.send(embed=embed)

	@commands.is_owner()
	@commands.command(name="restart")
	async def restart(_, ctx: Context) -> None:
		"""
		Restart the bot. This should only really be used when pulling changes to files such
		as `bot.py` and `main.py`.
		"""
		await ctx.send("Restarting!")
		os.execl(sys.executable, sys.executable, *sys.argv)

	@commands.is_owner()
	@commands.command(name="reload")
	async def reload(self, ctx: Context, ext: str) -> None:
		"""
		Reloads an extension.
		"""
		try:
			self.bot.reload_extension(f"cogs.{ext}")
			await ctx.send(f"The extension {ext} was reloaded.")
		except commands.ExtensionNotFound:
			await ctx.send(f"The extension {ext} doesn't exist.")
		except commands.ExtensionNotLoaded:
			await ctx.send(f"The extension {ext} is not loaded.")
		except commands.NoEntryPointError:
			await ctx.send(
				f"The extension {ext} doesn't have an entry point. (Try adding the setup function)"
			)
		except commands.ExtensionFailed as e:
			await ctx.send(f"Some unknown error happened while trying to reload extension {ext}.")
			print(e, file=stderr)

	@commands.is_owner()
	@commands.command(name="load")
	async def load(self, ctx: Context, ext: str) -> None:
		"""
		Loads an extension.
		"""
		try:
			self.bot.load_extension(f"cogs.{ext}")
			await ctx.send(f"The extension {ext} was loaded.")
		except commands.ExtensionNotFound:
			await ctx.send(f"The extension {ext} doesn't exist.")
		except commands.ExtensionAlreadyLoaded:
			await ctx.send(f"The extension {ext} is already loaded.")
		except commands.NoEntryPointError:
			await ctx.send(
				f"The extension {ext} doesn't have an entry point. (Try adding the setup function)"
			)
		except commands.ExtensionFailed as e:
			await ctx.send(f"Some unknown error happened while trying to reload extension {ext}.")
			print(e, file=stderr)

	@commands.is_owner()
	@commands.command(name="unload")
	async def unload(self, ctx: Context, ext: str) -> None:
		"""
		Unloads an extension.
		"""
		try:
			self.bot.unload_extension(f"cogs.{ext}")
			await ctx.send(f"The extension {ext} was unloaded.")
		except commands.ExtensionNotFound:
			await ctx.send(f"The extension {ext} doesn't exist.")
		except commands.ExtensionAlreadyLoaded:
			await ctx.send(f"The extension {ext} is already loaded.")
		except commands.NoEntryPointError:
			await ctx.send(
				f"The extension {ext} doesn't have an entry point. (Try adding the setup function)"
			)
		except commands.ExtensionFailed as e:
			await ctx.send(f"Some unknown error happened while trying to reload extension {ext}.")
			print(e, file=stderr)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Admin(bot))
