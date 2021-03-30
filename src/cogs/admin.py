from math import trunc
from subprocess import CompletedProcess, run
from sys import stderr
from traceback import print_exception, format_exception

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandError

from bot import SRBpp, execv
from cogs.src import RATE

PREFIX: str = "admin/bin"


class Admin(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx: Context, err: CommandError) -> None:
		"""
		A simple error handler to avoid spamming my console with errors
		I do not care about.
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
			await ctx.send("Invalid argument, please check your input and try again")
		else:  # TODO: Make it DM me the error maybe?
			print(f"{type(err)}: {err}", file=stderr)

			embed = discord.Embed(title=str(err), description=f"```py\n{''.join(format_exception(type(err), err, err.__traceback__))}```")
			embed.add_field(name="Command invoked: ", value=ctx.invoked_with)
			await ctx.author.send(f"{type(err)}", embed=embed)

			# For debugging purposes uncomment the following line to enable detailed error printing
			#print_exception(type(err), err, err.__traceback__, file=stderr)

	@commands.is_owner()
	@commands.command(name="compile", aliases=("make", "comp"))
	async def compile(_, ctx: Context) -> None:
		"""
		Run the bots Makefiles to update all the code.
		"""
		await execv(ctx, f"{PREFIX}/compile", TITLE="Compile")

	@commands.is_owner()
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

	@commands.is_owner()
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

	@commands.is_owner()
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

	@commands.is_owner()
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
