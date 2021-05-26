#!/usr/bin/env python3.9

"""
This program returns a complete list of all the runs awaiting verificaiton for a given game
(argv[1]) and optionally a second given game (argv[2]).
"""

from datetime import timedelta
from sys import argv, exit, stderr
from traceback import print_exception
from typing import Literal

from utils import *

USAGE: str = (
	"Usage: `+pending [GAME] [GAME (Optional)]`\n" + "Example: `+pending mkw mkwextracategories`"
)


def get_pending(game: str) -> list[dict]:
	_, gid = getgame(game)

	r = api_get(
		f"{API}/runs",
		params={
			"game": gid,
			"status": "new",
			"max": 200,
			"embed": "category,players,level",
			"orderby": "submitted",
		},
	)

	runs: list[dict] = []
	while True:
		runs.extend(r["data"])
		if "pagination" not in r or r["pagination"]["size"] < 200:
			break

		r = api_get(
			{item["rel"]: item["uri"] for item in r["pagination"]["links"]}["next"],
		)

	return runs


def main() -> int:
	if not (1 < len(argv) < 4):
		usage(USAGE)

	runs: list[dict] = []
	for game in argv[1:]:
		runs.extend(get_pending(game))

	if not runs:
		print("No pending runs found")
		return EXIT_SUCCESS

	print(
		"\n".join(
			f"[{run['level']['data']['name'] + ': ' + run['category']['data']['name'] if run['level']['data'] else run['category']['data']['name']}]({run['weblink']}) in `{str(timedelta(seconds=run['times']['primary_t'])).replace('000','')}` by {' and '.join([ player['name'] if player['rel'] == 'guest' else player['names']['international'] for player in run['players']['data']])}"
			for run in runs
		)
	)

	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
