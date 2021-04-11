#!/usr/bin/env python3.9

"""
This program gets the list of recent world records, and optionally gets only the
argv[1] most recent.
"""

from sys import argv, exit, stderr, stdout

import requests
from utils import *


def usage():
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print(
		"`+halo recent [AMOUNT (Optional)]`\n" + "Example: `+halo recent 5`",
		file=stderr,
	)
	exit(EXIT_FAILURE)


def main() -> int:
	# There is only one argument so idk if I need this
	# if len(argv) < 2:
	# 	usage()

	runs: list[Run] = requests.get(
		f"{API}/records/recent/{argv[1] if len(argv) > 1 else 10}"
	).json()
	for index in range(len(runs)):
		runs[index] = Run(runs[index])
	print(
		"\n".join(
			[
				f"`{run.game_name}, {run.level_name}` [{run.time}]({run.vid}) by {', '.join([player for player in run.runners])}"
				for run in runs
			]
		)
	)

	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
