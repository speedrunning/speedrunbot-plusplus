#!/usr/bin/env python3.9

"""
This program gets the number of runs verified and rejected by a given user (argv[1]) and optionally
limits the count to runs from 1 or 2 given games (argv[2] and argv[3]).
"""

import json
from collections import defaultdict
from datetime import datetime
from fcntl import LOCK_EX, LOCK_NB, LOCK_UN, flock
from io import TextIOWrapper
from itertools import count
from os.path import exists
from sys import argv, exit
from time import sleep

import requests
from requests import Session
from utils import *

TWO_HOURS = 7200
USAGE = (
	"Usage: `+verified [PLAYER NAME] [GAME (Optional)] [GAME (Optional)]`\n"
	+ "Example: `+verified AnInternetTroll mkw mkwextracategories`"
)


class xopen:
	"""
	A class that can be used similarly to open() that locks the file before reading or writing
	and releases the lock when done. This is useful to avoid things like +vlb from spawning
	multiple +verified processes that all try to access the cache at the same time.
	"""

	def __init__(self, filename: str, mode: str) -> None:
		self.filename = filename
		self.mode = mode
		self.file: TextIOWrapper = None

	def __enter__(self) -> TextIOWrapper:
		while True:
			try:
				self.file = open(self.filename, self.mode, encoding="utf-8")
				flock(self.file, LOCK_EX | LOCK_NB)
			except BlockingIOError:
				sleep(0.05)
			except OSError as e:
				error_and_die(e)
			else:
				return self.file

	def __exit__(self, _, __, ___) -> None:
		flock(self.file, LOCK_UN)
		self.file.close()


def xapi_get(session: Session, uri: str, params: Optional[dict[str, Any]] = {}) -> dict:
	"""
	A copy of what we have in utils.py but adapted for `requests.Session()`.
	"""
	while True:
		try:
			with session.get(uri, params=params) as r:
				if r.ok:
					return r.json()
				if r.status_code == RATE_LIMIT:
					sleep(5)
				else:
					try:
						error_and_die(r.json()["message"])
					except JSONDecodeError:
						error_and_die("The site is probably down go complain to ELO")
		except ConnectionError:
			sleep(2)


def check_cache_exists() -> None:
	"""
	A simple function to check if the cache file exists, and if it doesn't, to create it.
	"""
	if not exists(f"{CACHEDIR}/verified.json"):
		with xopen(f"{CACHEDIR}/verified.json", "w") as f:
			f.write("{}")


def write_to_cache(uid: str, totals: defaultdict) -> None:
	"""
	Writes the examination counts stored in the `totals` default dict to the cache.
	"""
	with xopen(f"{CACHEDIR}/verified.json", "r+") as f:
		data = json.load(f)

		if uid not in data:
			data[uid] = {}
		for game in totals:
			data[uid][game] = totals[game]

		data[uid]["last_updated"] = datetime.timestamp(datetime.utcnow())

		f.seek(0)
		json.dump(data, f, indent=8)
		f.truncate()


def fetch_runs(session: Session, uid: str, offset: int, totals: defaultdict) -> int:
	"""
	Takes a requests session and makes a request, adding the appropriate examination counts to
	the totals default dict. In the case of rate limiting it sleeps for 5 seconds and tries
	again.
	"""
	ret = 0
	while True:
		data = xapi_get(
			session, f"{API}/runs", params={"examiner": uid, "max": 200, "offset": offset}
		)

		for run in data["data"]:
			totals[run["game"]] += 1

		ret += data["pagination"]["size"]
		return ret


def make_requests(uid: str, gids: list[str]) -> int:
	"""
	Takes a user ID and a list of game IDs. Requests are made to get all the runs examined by
	the specified user and the totals for each game in the cache are updated. The number of
	examined runs for the game(s) specified by the user are then returned (or the total if none
	specified).
	"""
	totals: defaultdict = defaultdict(int)
	with requests.Session() as session:
		for i in count(0, 2000):
			tmp = 0
			for j in range(i, i + 2000, 200):
				tmp += fetch_runs(session, uid, j, totals)

			totals["total"] += tmp
			if tmp < 2000:
				break

	write_to_cache(uid, totals)
	if not gids:
		return totals["total"]
	return sum(totals[i] for i in gids)


def examined(uid: str, gids: list[str]) -> int:
	"""
	Gets the number of runs examined by the given user for the given games. If no games are
	specified then it gets all the users examined runs.
	"""
	check_cache_exists()
	with xopen(f"{CACHEDIR}/verified.json", "r") as f:
		data = json.load(f)

	try:
		then = data[uid]["last_updated"]
		now = datetime.timestamp(datetime.utcnow())
	except KeyError:  # User hasn't been added to cache yet
		return make_requests(uid, gids)

	if now - then > TWO_HOURS:
		return make_requests(uid, gids)

	if gids:
		try:
			return sum(data[uid][gid] for gid in gids)
		except KeyError:  # Counts for a specific game havent been added to cache yet
			return make_requests(uid, gids)
	return data[uid]["total"]


def getgids(games: list[str]) -> list[str]:
	"""
	Returns a list of game IDs for each game specified by the user.
	"""
	gids: list[str] = []
	for game in games:
		_, gid = getgame(game)
		gids.append(gid)

	return gids


def main() -> int:
	if not (1 < (argc := len(argv)) < 5):
		usage(USAGE)

	# Avoid the same game being passed twice
	if argc == 4 and argv[2] == argv[3]:
		argv.pop()

	uid = getuid(argv[1])
	gids = getgids(argv[2:])
	total = examined(uid, gids)

	print(f"Verified: {total}")
	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
