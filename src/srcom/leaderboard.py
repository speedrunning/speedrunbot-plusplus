#!/usr/bin/env python3.9

"""
This program returns the top 10 for a given game (argv[1]) as well as an
optional category (argv[2]) and optional subcategory (argv[3]).
"""

from re import sub
from sys import argv, exit, stderr
from typing import NoReturn, Type, Union

import requests
from utils import *


def usage() -> NoReturn:
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print(
		"Usage: `+leaderboard [GAME] [CATEGORY (Optional)] [SUBCATEGORY (Optional)]`\n"
		+ 'Example: `+leaderboard mkw "Nitro Tracks"`',
		file=stderr,
	)
	exit(EXIT_FAILURE)


def pad(time: str, ms: bool) -> str:
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
	if not ms:
		return time
	return f"{time}    " if "." not in time else time


def main() -> int:
	if not (1 < len(argv) <= 4):
		usage()

	# Get the games categories.
	try:
		game, gid = getgame(argv[1])
	except GameError as e:
		error_and_die(e)

	r = requests.get(f"{API}/games/{gid}/categories").json()
	cid = ""
	lflag = False

	try:
		cat = argv[2]
		cid = getcid(CAT, r)
		if not cid:
			r = requests.get(f"{API}/games/{GID}/levels").json()
			cid = getcid(CAT, r)
			lflag = True
		if not cid:
			error_and_die(f"Category with name '{cat}' not found.")
	except IndexError:  # Get default category if none supplied.
		try:
			cat = r["data"][0]["name"]
			cid = r["data"][0]["id"]
			if r["data"][0]["type"] == "per-level":
				r = requests.get(f"{API}/games/{gid}/levels").json()
				cid = r["data"][0]["id"]
				lflag = True
		except IndexError:
			error_and_die("The game '{game}' does not have any categories.")

	# Get top 10.
	try:
		vid, vval = subcatid(cid, argv[3], lflag)
	except IndexError:
		vid, vval = "", ""
	except (SubcatError, NotSupportedError) as e:
		error_and_die(e)

	if lflag:  # ILs.
		r = requests.get(f"{API}/levels/{cid}/categories").json()
		ilcid: str = r["data"][0]["id"]
		r = requests.get(
			f"{API}/leaderboards/{gid}/level/{cid}/{ilcid}?top=10&var-{vid}={vval}"
		).json()
	else:
		r = requests.get(
			f"{API}/leaderboards/{gid}/category/{cid}?top=10&var-{vid}={vval}"
		).json()

	# Set this flag if atleast one run has milliseconds.
	try:
		ms = "." in "".join(
			ptime(run["run"]["times"]["primary_t"]) for run in r["data"]["runs"]
		)
	except KeyError:
		error_and_die("The category '{CAT}' is an IL category, not level.")

	rows = tuple(
		(
			str(run["place"]),
			pad(ptime(run["run"]["times"]["primary_t"]), ms),
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

	title = f"Top {len(rows)}: {game} - {cat}" + (
		f" - {argv[3]}\n" if vid else "\n"
	)

	# Length of the longest run time, used for output padding.
	try:
		maxlen = max(len(i[1]) for i in rows)
	except ValueError:
		print(title + "No runs have been set in this category.")
		return EXIT_SUCCESS

	psize = len(r["data"]["runs"])
	print(
		title
		+ "```"
		+ "\n".join(
			f"{row[0].rjust(2).ljust(3)} {row[1].rjust(maxlen).ljust(maxlen + 1)} {row[2]}"
			for row in rows
		)
		+ (f"\n + {psize - 10} more" if psize > 10 else "")
		+ "```"
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
