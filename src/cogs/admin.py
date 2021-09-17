import asyncio
import os
import sys
from math import trunc
from subprocess import CompletedProcess, run
from sys import stderr
from traceback import format_exception, print_exception
from typing import Literal, Optional, Union

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandError
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

from bot import SRBpp, run_and_output
from cogs.src import RATE

PREFIX = "admin/bin"


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
		elif type(err) == commands.errors.NotOwner:
			await ctx.send("You are not allowed to use this command. ")
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

	async def compile(_, ctx: Union[Context, SlashContext], clean: Optional[str]) -> None:
		"""
		Run the bots Makefiles to update all the code.
		"""
		await run_and_output(ctx, f"{PREFIX}/compile", clean, title="Compile")

	@commands.is_owner()
	@commands.command(name="compile", aliases=("make", "comp"))
	async def compile_bot(self, ctx: Context, clean: Optional[str]) -> None:
		"""
		Run the bots Makefiles to update all the code.
		"""
		await self.compile(ctx, clean)

	@commands.is_owner()
	@cog_ext.cog_slash(
		name="compile",
		description="Run the bots Makefiles to update all the code.",
		options=[
			create_option(
				name="clean",
				description="Perform a `make clean` before `make`",
				option_type=5,
				required=True,
			)
		],
	)
	async def compile_slash(self, ctx: SlashContext, clean: bool) -> None:
		await self.compile(ctx, "clean" if clean else "")

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

	async def reload(self, ctx: Union[Context, SlashContext], ext: str) -> None:
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
	@cog_ext.cog_slash(
		name="reload",
		description="Reloads an extension.",
		options=[
			create_option(
				name="ext",
				description="The file name of an extension (without .py). For example `src`",
				option_type=3,
				required=True,
			),
		],
	)
	async def reload_slash(self, ctx: SlashContext, ext) -> None:
		await self.reload(ctx, ext)

	@commands.is_owner()
	@commands.command(name="reload")
	async def reload_bot(self, ctx: Context, ext: str) -> None:
		"""
		Reloads an extension.
		"""
		await self.reload(ctx, ext)

	async def load(self, ctx: Union[Context, SlashContext], ext: str) -> None:
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
	@commands.command(name="load")
	async def load_bot(self, ctx: Context, ext: str) -> None:
		"""
		Loads an extension.
		"""
		await self.load(self, ext)

	@commands.is_owner()
	@cog_ext.cog_slash(
		name="load",
		description="Reloads an extension.",
		options=[
			create_option(
				name="ext",
				description="The file name of an extension (without .py). For example `src`",
				option_type=3,
				required=True,
			),
		],
	)
	async def load_slash(self, ctx: SlashContext, ext: str) -> None:
		await self.load(ctx, ext)

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

	@commands.is_owner()
	@commands.command(name="unload")
	async def unload_bot(self, ctx: Context, ext: str) -> None:
		"""
		Unloads an extension.
		"""
		await self.unload(self, ext)

	@commands.is_owner()
	@cog_ext.cog_slash(
		name="unload",
		description="Unloads an extension.",
		options=[
			create_option(
				name="ext",
				description="The file name of an extension (without .py). For example `src`",
				option_type=3,
				required=True,
			),
		],
	)
	async def unload_slash(self, ctx: SlashContext, ext: str) -> None:
		await self.unload(ctx, ext)

	@commands.is_owner()
	@commands.command(name="announce", aliases=["announcement"])
	async def announce(self, ctx, *, message) -> None:
		channels = []
		messages = []
		for guild in self.bot.guilds:
			channels = guild.text_channels.sort(key=lambda channel: channel.position)
			for channel in channels:
				try:
					messages.append(channel.send(f"**Public announcement:**\n{message}"))
					break
				except discord.errors.Forbidden:
					continue
		await asyncio.gather(*messages)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Admin(bot))
