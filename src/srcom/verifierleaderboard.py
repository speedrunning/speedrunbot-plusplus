#!/usr/bin/env python3.9

import asyncio
from sys import argv, exit, stderr
from os import chdir, getcwd, system
from os.path import dirname

import requests
from utils import *


async def get_verified_runs(BASEDIR: str, USER: str, GAME: str) -> dict[str, int]:
	RETURNCODE, STDOUT, STDERR = await execv(f"{BASEDIR}/verified", USER, GAME)
	if RETURNCODE != EXIT_SUCCESS:
		print(STDERR, file=stderr)
		exit(RETURNCODE)
	else:
		return {
			"user": USER,
			"count": int(STDOUT.decode().replace("Verified: ", "")),
		}


def merge_mods(array1: list[dict], array2: list[dict]) -> list[dict]:
	results = []
	if not array2:
		return array1
	for i in array1:
		for ii in array2:
			if i["user"] == ii["user"]:
				results.append(
					{"user": i["user"], "count": i["count"] + ii["count"]}
				)
		if not results:
			results.extend(array2)
	return results


def usage() -> None:
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print(
		"Usage: `+verifierleaderboard [GAME]`\n"
		+ "\n Example: `+verifierleaderboard mkw`",
		file=stderr,
	)
	exit(EXIT_FAILURE)


async def main():
	if len(argv) < 2:
		usage()

	chdir(dirname(argv[0]))
	BASEDIR = getcwd()
	mods: list[dict] = []

	argv.pop(0)
	for game in argv:
		# F one liner
		# mods = sorted(merge_mods(await asyncio.gather(*[get_verified_runs(mod, game) for mod in [mod["names"]["international"] for mod in requests.get(f"{API}/games", params={"abbreviation": game, "embed": "moderators"}).json()["data"][0]["moderators"]["data"]]]), mods), key=lambda k: k["count"], reverse=True)
		game_dict = requests.get(
			f"{API}/games", params={"abbreviation": game, "embed": "moderators"}
		).json()

		if not game_dict["data"]:
			print(f"Error: Game `{game}` not found", file=stderr)
			exit(EXIT_FAILURE)

		if not game_dict["data"][0]["moderators"]["data"]:
			print(f"Error: The game {game} has no moderators", file=stderr)
			exit(EXIT_FAILURE)

		mods = sorted(
			merge_mods(
				await asyncio.gather(
					*[
						get_verified_runs(BASEDIR, mod, game)
						for mod in [
							mod["names"]["international"]
							for mod in game_dict["data"][0]["moderators"][
								"data"
							]
						]
					]
				),
				mods,
			),
			key=lambda k: k["count"],
			reverse=True,
		)

	MAXLEN_USER: int = max(len(i["user"]) for i in mods)
	print(
		"```\n"
		+ "\n".join(
			[
				f"{str(i + 1).rjust(2).ljust(3)} {mods[i]['user'].ljust(MAXLEN_USER).rjust(MAXLEN_USER + 1)}  {str(mods[i]['count']).ljust(2).rjust(4)}"
				for i in range(len(mods))
			]
		)
		+ "\n```"
	)


if __name__ == "__main__":
	asyncio.run(main())
