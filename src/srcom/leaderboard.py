#!/usr/bin/env python3.9

"""
This program returns the top 10 for a given game (argv[1]) as well as an
optional category (argv[2]) and optional subcategory (argv[3]).
"""

from re import sub
from sys import argv, exit, stderr
from typing import Iterable

import requests
from utils import *


def pad(TIME: str, MS: bool) -> str:
	"""
	Pad a time with blank spaces if it doesnt contain milliseconds for
	output formatting.

	>>> pad("59:54.397", True)
	'59:54.397'
	>>> pad("3:42", True)
	'3:42    '
	>>> pad("1:39", False)
	'1:39'
	"""
	if not MS:
		return TIME
	return f"{TIME}    " if "." not in TIME else TIME


def main() -> int:
	CAT: str
	GAME: str
	GID: str

	# Get the games categories
	GAME, GID = game(argv[1])
	r: dict = requests.get(f"{API}/games/{GID}/categories").json()
	cid: str = None

	try:
		CAT = argv[2]
		for c in r["data"]:
			if c["name"] == CAT:
				cid = c["id"]
				break
	# Get default category if none supplied
	except IndexError:
		for c in r["data"]:
			if c["type"] == "per-game":
				CAT = c["name"]
				cid = c["id"]
				break

	# TODO: Support levels
	if not cid:
		return EXIT_FAILURE

	# Get top 10
	VID: str
	VVAL: str
	try:
		VID, VVAL = subcatid(cid, argv[3])
	except IndexError:
		VID, VVAL = "", ""
	except SubcatError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	r = requests.get(
		f"{API}/leaderboards/{GID}/category/{cid}?top=10&var-{VID}={VVAL}"
	).json()

	# Set this flag if atleast one run has milliseconds.
	MS: bool = "." in "".join(
		ptime(run["run"]["times"]["primary_t"]) for run in r["data"]["runs"]
	)

	ROWS: tuple[Iterable[str], ...] = tuple(
		(
			str(run["place"]),
			pad(ptime(run["run"]["times"]["primary_t"]), MS),
			", ".join(
				username(player["id"])
				if player["rel"] == "user"
				else sub("^\[.*\]", "", player["name"])  # Regex to remove flags
				for player in run["run"]["players"]
			),
		)
		for run in r["data"]["runs"]
	)

	# Length of the longest run time, used for output padding
	MAXLEN: int = max(len(i[1]) for i in ROWS)

	print(
		f"Top {len(ROWS)}: {GAME} - {CAT}"
		+ (f" - {argv[3]}\n" if VID else "\n")
		+ "```"
		+ "\n".join(
			f"{row[0].rjust(2).ljust(3)} {row[1].rjust(MAXLEN).ljust(MAXLEN + 1)} {row[2]}"
			for row in ROWS
		)
		+ "```"
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
