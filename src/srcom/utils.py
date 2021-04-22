#!/usr/bin/env python3.9

"""
This file contains all sorts of variables and utilities used in the sr.c
related programs.
"""

import asyncio
import shlex
from sys import exit, stderr
from typing import Literal, NoReturn, Optional, Type, Union

import requests

API: Literal[str] = "https://www.speedrun.com/api/v1"

EXIT_SUCCESS: Literal[int] = 0
EXIT_FAILURE: Literal[int] = 1


class UserError(Exception):
	"""Raised when trying to access a user that does not exist."""


class GameError(Exception):
	"""Raised when trying to access a game that does not exist."""


class SubcatError(Exception):
	"""Raised when trying to get a subcategory that does not exist."""


class NotSupportedError(Exception):
	"""Raised when trying to use a feature that is not yet supported."""


def error_and_die(e: Union[Type[Exception], str]) -> NoReturn:
	"""
	Print an error message to the stderr and then exit.
	"""
	print(f"Error: {e}", file=stderr)
	exit(EXIT_FAILURE)


def getuid(user: str) -> str:
	"""
	Get a users user ID from their username.

	>>> getuid("1")
	'zx7gd1yx'
	>>> getuid("AnInternetTroll")
	'7j477kvj'
	>>> getuid("abc")
	Traceback (most recent call last):
		...
	utils.UserError: User with username 'abc' not found.
	"""

	r = requests.get(f"{API}/users/{user}").json()
	try:
		return r["data"]["id"]
	except KeyError:
		raise UserError(f"User with username '{user}' not found.")


def username(uid: str) -> str:
	"""
	Get a users username from their user ID.

	>>> username("zx7gd1yx")
	'1'
	>>> username("7j477kvj")
	'AnInternetTroll'
	>>> username("Sesame Street")
	Traceback (most recent call last):
		...
	utils.UserError: User with uid 'Sesame Street' not found.
	"""
	r = requests.get(f"{API}/users/{uid}").json()
	try:
		return r["data"]["names"]["international"]
	except KeyError:
		raise UserError(f"User with uid '{uid}' not found.")


def getgame(abbrev: str) -> tuple[str, str]:
	"""
	Get a games name and game ID from their abbreviation.

	>>> getgame("mkw")
	('Mario Kart Wii', 'l3dxogdy')
	>>> getgame("celestep8")
	('CELESTE Classic', '4d7e7z67')
	>>> getgame("Fake Game")
	Traceback (most recent call last):
		...
	utils.GameError: Game with abbreviation 'Fake Game' not found.
	"""
	r = requests.get(f"{API}/games?abbreviation={abbrev}").json()
	try:
		gid: str = r["data"][0]["id"]
		gname: str = r["data"][0]["names"]["international"]
		return (gname, gid)
	except IndexError:
		raise GameError(f"Game with abbreviation '{abbrev}' not found.")


def subcatid(cid: str, subcat: str, lflag: bool = False) -> tuple[str, str]:
	"""
	Get the subcategory ID and and value ID from the given category ID and
	subcategory value label. Whoever decided to handle subcategories like
	this should consider switching professions.

	>>> subcatid("w20gmyzk", "Random Seed")
	('5ly7759l', '5q804wk1')
	>>> subcatid("wk68zp21", "Skips")
	('j84rwjl9', '81p4xxg1')
	>>> subcatid("xd130359", "Mobile", True)
	('ylqmdmvn', '810enwwq')
	>>> subcatid("mkeoz98d", "Gem Skips")
	Traceback (most recent call last):
		...
	utils.SubcatError: Subcategory with label 'Gem Skips' not found.
	"""
	r = requests.get(
		f"{API}/{'levels' if LFLAG else 'categories'}/{CID}/variables"
	).json()
	lsubcat = subcat.lower()
	try:
		for var in r["data"]:
			if var["is-subcategory"]:
				for v in var["values"]["values"]:
					if var["values"]["values"][v]["label"].lower() == lsubcat:
						return (var["id"], v)
	except KeyError:  # TODO: Test if this is still required after Ziro's PR.
		raise SubcatError(f"Subcategory with label '{SUBCAT}' not found.")
		# raise NotSupportedError(f"Subcategories are not yet supported for ILs.")
	raise SubcatError(f"Subcategory with label '{SUBCAT}' not found.")


def ptime(s: float) -> str:
	"""
	Pretty print a time in the format H:M:S.ms. Empty leading fields are
	disgarded with the exception of times under 60 seconds which show 0
	minutes.

	>>> ptime(234.2)
	'3:54.200'
	>>> ptime(23275.24)
	'6:27:55.240'
	>>> ptime(51)
	'0:51'
	>>> ptime(325)
	'5:25'
	"""
	m, s = divmod(s, 60)
	h, m = divmod(m, 60)
	ms = int(round(s % 1 * 1000))

	if not h:
		if not ms:
			return "{}:{:02d}".format(int(m), int(s))
		return "{}:{:02d}.{:03d}".format(int(m), int(s), ms)
	if not ms:
		return "{}:{:02d}:{:02d}".format(int(h), int(m), int(s))
	return "{}:{:02d}:{:02d}.{:03d}".format(int(h), int(m), int(s), ms)


def getcid(cat: str, r: dict) -> Optional[str]:
	"""
	Get the category ID with the name `CAT` from the request `R`. This
	function doesn't do the request itself, since it's meant to work with
	both fullgame and IL's, amongst other reasons.

	>>> r: dict = requests.get(f"{API}/games/l3dxogdy/categories").json()
	>>> getcid("Nitro Tracks", r)
	'7kj6mz23'
	>>> getcid("Retro Tracks", r)
	'xk9v3gd0'
	>>> r = requests.get(f"{API}/games/l3dxogdy/levels").json()
	>>> getcid("This game has no levels", r)
	>>> r = requests.get(f"{API}/games/4d7e7z67/levels").json()
	>>> getcid("100m", r)
	'rdn25e5d'
	"""
	lcat = cat.lower()
	for c in r["data"]:
		if c["name"].lower() == lcat:
			return c["id"]
	return None
