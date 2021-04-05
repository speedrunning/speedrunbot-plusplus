#!/usr/bin/env python3.9

from datetime import timedelta
from sys import argv, exit, stderr
from traceback import print_exception

import requests
from utils import *

GAME: str
GID: str


def usage() -> None:
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print(
		"Usage: `+pending [GAME]`\n" + "Example: `+pending mkw`",
		file=stderr,
	)
	exit(EXIT_FAILURE)


def main() -> int:
	if not (1 < len(argv) <= 4):
		usage()

	try:
		GAME, GID = game(argv[1])
	except GameError as e:
		print(f"Error: {e}", file=stderr)
		return EXIT_FAILURE
	runs = []
	temp = requests.get(
		f"{API}/runs",
		params={
			"game": GID,
			"status": "new",
			"max": 200,
			"embed": "category,players,level",
			"orderby": "submitted",
		},
	)
	while True:
		temp_json = temp.json()
		runs.extend(temp_json["data"])
		if (
			"pagination" not in temp_json
			or temp_json["pagination"]["size"] < 200
		):
			break
		temp = requests.get(
			{
				item["rel"]: item["uri"]
				for item in temp_json["pagination"]["links"]
			}["next"],
		)
	if len(runs) == 0:
		print("No pending runs found")
		return EXIT_SUCCESS
	for run in runs:
		print(
			f"[{run['level']['data']['name'] + ': ' + run['category']['data']['name'] if run['level']['data'] else run['category']['data']['name']}]({run['weblink']}) in `{str(timedelta(seconds=run['times']['primary_t'])).replace('000','')}` by {' and '.join([ player['name'] if player['rel'] == 'guest' else player['names']['international'] for player in run['players']['data']])}"
		)

	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
