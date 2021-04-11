#!/usr/bin/env python3.9

"""
This program gets the current world record for a given game (argv[1]) and
optionally a specific category (argv[2]) and subcategories (argv[3..]).
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
		"`+halo recent [AMMOUNT (Optional)]`\n" + "Example: `+halo recent 5`",
		file=stderr,
	)
	exit(EXIT_FAILURE)


def main():
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


if __name__ == "__main__":
	main()
