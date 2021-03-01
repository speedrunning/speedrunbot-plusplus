#!/usr/bin/env python3.9

"""
This program gets the number of runs that a given player (argv[1]) has set.
"""

import asyncio
import concurrent.futures
from itertools import count
from sys import argv, exit

import requests
from utils import *


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
			loop = asyncio.get_event_loop()
			futures = (
				loop.run_in_executor(
					executor,
					requests.get,
					f"{API}/runs?user={UID}&max=200&offset={offset}",
				)
				for offset in range(offstart, offstart + 1000, 200)
			)
			for response in await asyncio.gather(*futures):
				r: dict = response.json()
				if len(r["data"]) == 0:
					return (fullgame, il)

				for run in r["data"]:
					if run["level"] is None:
						fullgame += 1
					else:
						il += 1


def main() -> int:
	try:
		UID = uid(argv[1])
	except UserError:
		return EXIT_FAILURE

	loop = asyncio.get_event_loop()
	fullgame, il = loop.run_until_complete(runs(UID))

	print(
		f"Full Game: {fullgame}\n"
		+ f"Individual Level: {il}\n"
		+ f"Total: {fullgame + il}"
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	ret: int = main()
	exit(ret)
