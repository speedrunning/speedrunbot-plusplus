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

CAT: str
GAME: str
GID: str
VID: str
VVAL: str


def usage() -> None:
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print(
		"Usage: `+leaderboard [GAME] [CATEGORY (Optional)] [SUBCATEGORY (Optional)]`\n"
		+ 'Example: `+leaderboard mkw "Nitro Tracks"`'
	)
	exit(EXIT_FAILURE)


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
	if not (1 < len(argv) <= 4):
		usage()

	# Get the games categories.
	try:
		GAME, GID = game(argv[1])
	except GameError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	r: dict = requests.get(f"{API}/games/{GID}/categories").json()
	cid: str = None
	lflag: bool = False

	try:
		CAT = argv[2]
		cid = getcid(CAT, r)
		if not cid:
			r = requests.get(f"{API}/games/{GID}/levels").json()
			cid = getcid(CAT, r)
			lflag = True
		if not cid:
			print(f"Error: Category with name '{CAT}' not found.", file=stderr)
			return EXIT_FAILURE
	# Get default category if none supplied.
	except IndexError:
		try:
			CAT = r["data"][0]["name"]
			cid = r["data"][0]["id"]
			if r["data"][0]["type"] == "per-level":
				r = requests.get(f"{API}/games/{GID}/levels").json()
				cid = r["data"][0]["id"]
				lflag = True
		except IndexError:
			print(
				f"Error: The game '{GAME}' does not have any categories.",
				file=stderr,
			)
			return EXIT_FAILURE

	# Get top 10.
	try:
		VID, VVAL = subcatid(cid, argv[3], lflag)
	except IndexError:
		VID, VVAL = "", ""
	except (SubcatError, NotSupportedError) as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	if lflag:  # ILs.
		r = requests.get(f"{API}/levels/{cid}/categories").json()
		ILCID: str = r["data"][0]["id"]
		r = requests.get(
			f"{API}/leaderboards/{GID}/level/{cid}/{ILCID}?top=10&var-{VID}={VVAL}"
		).json()
	else:
		r = requests.get(
			f"{API}/leaderboards/{GID}/category/{cid}?top=10&var-{VID}={VVAL}"
		).json()

	# Set this flag if atleast one run has milliseconds.
	try:
		MS: bool = "." in "".join(
			ptime(run["run"]["times"]["primary_t"]) for run in r["data"]["runs"]
		)
	except KeyError:
		print(
			f"Error: The category '{CAT}' is an IL category, not level.",
			file=stderr,
		)
		return EXIT_FAILURE

	ROWS: tuple[Iterable[str], ...] = tuple(
		(
			str(run["place"]),
			pad(ptime(run["run"]["times"]["primary_t"]), MS),
			", ".join(
				username(player["id"])
				if player["rel"] == "user"
				else sub(
					"^\[.*\]", "", player["name"]
				)  # Regex to remove flags.
				for player in run["run"]["players"]
			),
		)
		for run in r["data"]["runs"][:10]
	)

	TITLE: str = f"Top {len(ROWS)}: {GAME} - {CAT}" + (
		f" - {argv[3]}\n" if VID else "\n"
	)

	# Length of the longest run time, used for output padding.
	try:
		MAXLEN: int = max(len(i[1]) for i in ROWS)
	except ValueError:
		print(TITLE + "No runs have been set in this category.")
		return EXIT_SUCCESS

	PSIZE: int = len(r["data"]["runs"])
	print(
		TITLE
		+ "```"
		+ "\n".join(
			f"{row[0].rjust(2).ljust(3)} {row[1].rjust(MAXLEN).ljust(MAXLEN + 1)} {row[2]}"
			for row in ROWS
		)
		+ (f"\n + {PSIZE - 10} more" if PSIZE > 10 else "")
		+ "```"
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
