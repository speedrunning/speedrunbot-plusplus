#!/usr/bin/env python3.9

"""
This program gets the number of runs that a given user (argv[1]) has verified
or rejected.
"""

import asyncio
import concurrent.futures
from asyncio.events import AbstractEventLoop
from itertools import count
from sys import argv, exit, stderr
from typing import Awaitable, Iterable

import requests
from utils import *


async def verified(UID: int) -> int:
	"""
	Get the number of runs verified/rejected by a user with the user id
	`UID`. Each request can only return at most 200 runs, and because this
	command is generally going to be used to track mods/verifiers with
	thousands of runs verified, 25 requests are done in parallel. If none of
	the 25 requests have less than 200 runs in them (meaning there are more
	runs), another 25 requests are made until the condition is met.

	>>> loop = asyncio.get_event_loop()
	>>> loop.run_until_complete(verified("zx7gd1yx")) > 2000
	True
	>>> loop.run_until_complete(verified("8r72e1qj"))
	0
	>>> loop.run_until_complete(verified("jn39g1qx")) > 4000
	True
	"""
	runcount: int = 0

	for offstart in count(0, 5000):
		with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
			loop: AbstractEventLoop = asyncio.get_event_loop()
			futures: Iterable[Awaitable] = (
				loop.run_in_executor(
					executor,
					requests.get,
					f"{API}/runs?examiner={UID}&max=200&offset={offset}",
				)
				for offset in range(offstart, offstart + 5000, 200)
			)
			for response in await asyncio.gather(*futures):
				r: dict = response.json()
				size: int = r["pagination"]["size"]
				if size < 200:
					return runcount + size

				runcount += size


def main() -> int:
	try:
		UID: str = uid(argv[1])
	except UserError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	LOOP: AbstractEventLoop = asyncio.get_event_loop()
	VERIFIED: int = LOOP.run_until_complete(verified(UID))

	print(f"Verified: {VERIFIED}")
	return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
