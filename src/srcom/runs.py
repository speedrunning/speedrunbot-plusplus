#!/usr/bin/env python3.9

"""
This program gets the number of runs that a given player (argv[1]) has set.
"""

import asyncio
import concurrent.futures
from asyncio.events import AbstractEventLoop
from itertools import count
from sys import argv, exit, stderr
from typing import Awaitable, Iterator

import requests
from utils import *

FULLGAME: int
IL: int


def usage() -> None:
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print("Usage: `+runs [PLAYER NAME]`\n" + "Example: `+runs AnInternetTroll`")
	exit(EXIT_FAILURE)


async def runs(UID: int) -> tuple[int, int]:
	"""
	Get the number of runs by a user with the user id `UID`. This function
	works exactly the same as the one in `verified.py`, so read the
	docstring for that one if you care about how it works.

	>>> loop = asyncio.get_event_loop()
	>>> loop.run_until_complete(runs("v81ggnp8"))
	(1148, 458)
	>>> loop.run_until_complete(runs("8r72e1qj"))
	(2, 0)
	>>> loop.run_until_complete(runs("68w0rrlj"))
	(55, 9)
	"""
	fullgame: int = 0
	il: int = 0

	for offstart in count(0, 1000):
		with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
			loop: AbstractEventLoop = asyncio.get_event_loop()
			futures: Iterator[Awaitable] = (
				loop.run_in_executor(
					executor,
					requests.get,
					f"{API}/runs?user={UID}&max=200&offset={offset}",
				)
				for offset in range(offstart, offstart + 1000, 200)
			)
			for response in await asyncio.gather(*futures):
				r: dict = response.json()
				size: int = r["pagination"]["size"]
				for run in r["data"]:
					if run["level"]:
						il += 1
					else:
						fullgame += 1

				if size < 200:
					return (fullgame, il)


def main() -> int:
	if len(argv) != 2:
		usage()

	try:
		UID = uid(argv[1])
	except UserError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	LOOP: AbstractEventLoop = asyncio.get_event_loop()
	FULLGAME, IL = LOOP.run_until_complete(runs(UID))

	print(
		f"Full Game: {FULLGAME}\n"
		+ f"Individual Level: {IL}\n"
		+ f"Total: {FULLGAME + IL}"
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
