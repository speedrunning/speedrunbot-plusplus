#!/usr/bin/env python3.9

from datetime import timedelta
from sys import argv, exit, stderr
from traceback import print_exception
from typing import NoReturn

import requests
from utils import *


def usage() -> NoReturn:
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print(
		"Usage: `+pending [GAME]`\n" + "Example: `+pending mkw`",
		file=stderr,
	)
	exit(EXIT_FAILURE)


def get_pending(game: str) -> list[dict]:
	try:
		_, gid = getgame(game)
	except GameError as e:
		error_and_die(e)

	r = requests.get(
		f"{API}/runs",
		params={
			"game": gid,
			"status": "new",
			"max": 200,
			"embed": "category,players,level",
			"orderby": "submitted",
		},
	)

	if r.status_code not in (200, 204):
		error_and_die(f"{r.json()['message']} (Error code {r.status_code})")

	runs: list[dict] = []
	while True:
		r_json = r.json()
		runs.extend(r_json["data"])
		if "pagination" not in r_json or r_json["pagination"]["size"] < 200:
			break

		r = requests.get(
			{
				item["rel"]: item["uri"]
				for item in r_json["pagination"]["links"]
			}["next"],
		)

	return runs


def main() -> int:
	if not (1 < len(argv) < 4):
		usage()

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
