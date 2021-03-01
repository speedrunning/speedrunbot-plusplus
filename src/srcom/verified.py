#!/usr/bin/env python3.9

"""
This program gets the number of runs that a given user (argv[1]) has verified
or rejected.
"""

import asyncio
import concurrent.futures
from itertools import count
from sys import argv, exit

import requests
from utils import *


async def verified(UID: int) -> int:
	"""
	Get the number of runs verified/rejected by a user with the user id `UID`.
	Each request can only return at most 200 runs, and because this command is
	generally going to be used to track mods/verifiers with thousands of runs
	verified, 25 requests are done in parallel. If none of the 25 requests have
	0 runs in them (meaning all runs have been seen), another 25 requests are
	made until the condition is met.

	>>> loop = asyncio.get_event_loop()
	>>> loop.run_until_complete(verified("zx7gd1yx")) > 2000
	True
	>>> loop.run_until_complete(verified("8r72e1qj"))
	0
	>>> loop.run_until_complete(verified("jn39g1qx")) > 4000
	True
	"""
	runs: list[list] = []

	for offstart in count(0, 5000):
		with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
			loop = asyncio.get_event_loop()
			futures = (
				loop.run_in_executor(
					executor,
					requests.get,
					f"{API}/runs?examiner={UID}&max=200&offset={offset}",
				)
				for offset in range(offstart, offstart + 5000, 200)
			)
			for response in await asyncio.gather(*futures):
				r: dict = response.json()
				if len(r["data"]) == 0:
					return len(runs)

				runs.extend(response.json()["data"])


def main() -> int:
	try:
		UID: str = uid(argv[1])
	except UserError:
		return EXIT_FAILURE

	loop = asyncio.get_event_loop()
	VERIFIED: int = loop.run_until_complete(verified(UID))

	print(f"Verified: {VERIFIED}")
	return EXIT_SUCCESS


if __name__ == "__main__":
	ret: int = main()
	exit(ret)
