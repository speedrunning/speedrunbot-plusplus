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


async def queue(GID: str) -> int:
	"""
	Get the number of runs in the queue of the game with ID `GID`. Since
	each request can only return at most 200 runs, 5 requests of 200 runs
	are done in parallel. If none of the requests have less than 200 runs,
	additional series of 5 requests are made until the condition is met.
	"""
	runcount: int = 0

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
	                        runcount += size
	                        if size < 200:
	                                return runcount


def main() -> int:
	try:
		GID: str = game(argv[1])[1]
	except GameError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	LOOP: AbstractEventLoop = asyncio.get_event_loop()
	LENGTH: int = LOOP.run_until_complete(queue(GID))

	print(f"Queue Length: {LENGTH}")
	return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
