#!/usr/bin/env python3.9

"""
This program gets the current world record for a given game (argv[1]) and
optionally a specific category (argv[2]) and subcategories (argv[3..]).
"""

from re import sub
from sys import argv, exit, stderr

import requests
from utils import *

GAME: str
GID: str
CAT: str
VID: str
VVAL: str
VIDEOS: Union[list[dict[str, str]], None]


def usage() -> None:
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print(
		"Usage: `+worldrecord [GAME] [CATEGORY (Optional)] [SUBCATEGORY (Optional)]`\n"
		+ 'Example: `+worldrecord mkw "Nitro Tracks"`'
	)
	exit(EXIT_FAILURE)


def main() -> int:
	if 1 < len(argv) <= 4:
		usage()

	# Get the game ID and name.
	try:
		GAME, GID = game(argv[1])
	except GameError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	# Get the games categories.
	r = requests.get(f"{API}/games/{GID}/categories").json()
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
				lflag = True
		except IndexError:
			print(
				f"Error: The game '{argv[1]}' does not have any categories.", file=stderr
			)
			return EXIT_FAILURE

	# Get WR.
	try:
		VID, VVAL = subcatid(cid, argv[3])
	except IndexError:
		VID, VVAL = "", ""
	except (SubcatError, NotSupportedError) as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	if lflag:  # ILs.
		r = requests.get(f"{API}/levels/{cid}/categories").json()
		ILCID: str = r["data"][0]["id"]
		r = requests.get(
			f"{API}/leaderboards/{GID}/level/{cid}/{ILCID}?top=10"
		).json()
	else:
		r = requests.get(
			f"{API}/leaderboards/{GID}/category/{cid}?top=10&var-{VID}={VVAL}"
		).json()

	WR: dict = r["data"]["runs"][0]["run"]
	TIME: str = ptime(WR["times"]["primary_t"])
	PLAYERS: str = ", ".join(
		username(player["id"])
		if player["rel"] == "user"
		else sub("^\[.*\]", "", player["name"])  # Regex to remove flags.
		for player in WR["players"]
	)
	try:
		VIDEOS = WR["videos"]["links"]
	except TypeError:  # No video.
		VIDEOS = None

	print(
		f"World Record: {GAME} - {CAT}"
		+ (f" - {argv[3]}\n" if VID else "\n")
		+ f"{TIME}  {PLAYERS}\n"
		+ (
			"\n".join(f"<{r['uri']}>" for r in VIDEOS)
			if type(VIDEOS) == list
			else "No video available."
		)
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
