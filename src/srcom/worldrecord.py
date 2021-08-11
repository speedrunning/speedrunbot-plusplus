#!/usr/bin/env python3.9

"""
This program gets the current world record for a given game (argv[1]) and optionally a specific
category (argv[2]) and subcategories (argv[3..]).
"""

from re import sub
from sys import argv, exit, stderr
from typing import Literal, Optional

from utils import *

USAGE: str = (
	"Usage: `+worldrecord [GAME] [CATEGORY (Optional)] [SUBCATEGORY (Optional)]`\n"
	+ 'Example: `+worldrecord mkw "Nitro Tracks"`'
)


def main() -> int:
	if not (1 < len(argv) <= 4):
		usage(USAGE)

	game, gid = getgame(argv[1])

	# Get the games categories.
	r = api_get(f"{API}/games/{gid}/categories")
	cid = ""
	lflag = False

	try:
		cat = argv[2]
		cid = getcid(cat, r)
		if not cid:  # No matching fullgame cat, so check ILs.
			r = api_get(f"{API}/games/{gid}/levels")
			cid = getcid(cat, r)
			lflag = True
		if not cid:
			error_and_die(f"Category with name '{cat}' not found.")
	except IndexError:  # Get default category if none supplied.
		try:
			cat = r["data"][0]["name"]
			cid = r["data"][0]["id"]
			if r["data"][0]["type"] == "per-level":
				r = api_get(f"{API}/games/{gid}/levels")
				cat = r["data"][0]["name"]
				cid = r["data"][0]["id"]
				lflag = True
		except IndexError:
			error_and_die(f"The game '{argv[1]}' does not have any categories.")

	# Get WR.
	try:
		vid, vval = subcatid(cid, argv[3], lflag)
	except IndexError:
		vid, vval = "", ""

	if lflag:  # ILs.
		r = api_get(f"{API}/levels/{cid}/categories")
		ilcid: str = r["data"][0]["id"]
		r = api_get(
			f"{API}/leaderboards/{gid}/level/{cid}/{ilcid}",
			params={"top": 1, f"var-{vid}": vval},
		)
	else:
		r = api_get(
			f"{API}/leaderboards/{gid}/category/{cid}",
			params={"top": 1, f"var-{vid}": vval},
		)

	title = f"World Record: {game} - {cat}" + (f" - {argv[3]}\n" if vid else "\n")
	try:
		wr: dict = r["data"]["runs"][0]["run"]
	except KeyError:
		error_and_die(f"The category '{cat}' is an IL category, not level.")
	except IndexError:
		print(title + "No runs have been set in this category.")
		return EXIT_SUCCESS

	time = ptime(wr["times"]["primary_t"])
	players = ", ".join(
		username(player["id"])
		if player["rel"] == "user"
		else sub("^\[.*\]", "", player["name"])  # Regex to remove flags.
		for player in wr["players"]
	)

	videos: Optional[list[dict[str, str]]]
	try:
		videos = wr["videos"]["links"]
	except TypeError:  # No video.
		videos = None

	print(
		title
		+ f"{time}  {players}\n"
		+ (
			"\n".join(f"<{r['uri']}>" for r in videos)
			if type(videos) == list
			else "No video available."
		)
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
