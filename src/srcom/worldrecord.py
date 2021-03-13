#!/usr/bin/env python3.9

"""
This program gets the current world record for a given game (argv[1]) and
optionally a specific category (argv[2]) and subcategories (argv[3..]).
"""

from re import sub
from sys import argv, exit, stderr

import requests
from utils import *


def main() -> int:
	# Get the game ID and name
	GAME: str
	GID: str
	try:
		GAME, GID = game(argv[1])
	except GameError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE

	# Get the games categories
	r = requests.get(f"{API}/games/{GID}/categories").json()
	CAT: str
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

	# Get WR
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
		f"{API}/leaderboards/{GID}/category/{cid}?top=1&var-{VID}={VVAL}"
	).json()

	WR: dict = r["data"]["runs"][0]["run"]
	TIME: str = ptime(WR["times"]["primary_t"])
	PLAYERS: str = ", ".join(
		username(player["id"])
		if player["rel"] == "user"
		else sub("^\[.*\]", "", player["name"])  # Regex to remove flags
		for player in WR["players"]
	)
	VIDEOS: list[dict[str, str]] = WR["videos"]["links"]

	print(
		f"World Record: {GAME} - {CAT}\n"
		+ f"{TIME}  {PLAYERS}\n"
		+ "\n".join(f"<{r['uri']}>" for r in VIDEOS)
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
