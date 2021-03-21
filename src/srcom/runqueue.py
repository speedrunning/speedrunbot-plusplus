#!/usr/bin/env python3.9

"""
This program gets the number of runs in the verification queue of a given game
(argv[1]).
"""

import asyncio
import concurrent.futures
from asyncio.events import AbstractEventLoop
from itertools import count
from sys import argv, exit, stderr
from typing import Awaitable, Iterable

import requests
from utils import *


async def queue(GID: str) -> tuple[int, int]:
	"""
	Get the number of runs in the queue of the game with ID `GID`. Since
	each request can only return at most 200 runs, 5 requests of 200 runs
	are done in parallel. If none of the requests have less than 200 runs,
	additional series of 5 requests are made until the condition is met.
	"""
	fullgame: int = 0
	il: int = 0

	for offstart in count(0, 1000):
		with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
			loop: AbstractEventLoop = asyncio.get_event_loop()
			futures: Iterable[Awaitable] = (
				loop.run_in_executor(
					executor,
					requests.get,
					f"{API}/runs?game={GID}&status=new&max=200&offset={offset}",
				)
				for offset in range(offstart, offstart + 1000, 200)
			)
			for response in await asyncio.gather(*futures):
				r: dict = response.json()
				size: int = len(r["data"])
				for run in r["data"]:
					if run["level"]:
						il += 1
					else:
						fullgame += 1

				if size < 200:
					return (fullgame, il)


def main() -> int:
	try:
		GID: str = game(argv[1])[1]
	except GameError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	LOOP: AbstractEventLoop = asyncio.get_event_loop()

	FULLGAME: int
	IL: int
	FULLGAME, IL = LOOP.run_until_complete(queue(GID))

	print(
		f"Fullgame: {FULLGAME}\n"
		+ f"Individual Level: {IL}\n"
		+ f"Total: {FULLGAME + IL}"
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
