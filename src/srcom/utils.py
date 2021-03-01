#!/usr/bin/env python3.9

"""
This file contains all sorts of variables and utilities used in the sr.c
related programs.
"""

import requests

API: str = "https://www.speedrun.com/api/v1"

EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1


class UserError(Exception):
	"""Raised when trying to access a user that does not exist"""


class GameError(Exception):
	"""Raised when trying to access a game that does not exist"""


def uid(USER: str) -> str:
	"""
	Get a users user ID from their username. Returns None on error.

	>>> uid("1")
	'zx7gd1yx'
	>>> uid("AnInternetTroll")
	'7j477kvj'
	>>> uid("abc")
	Traceback (most recent call last):
	    ...
	utils.UserError: User with username 'abc' not found.
	"""

	R: dict = requests.get(f"{API}/users/{USER}").json()
	try:
		return R["data"]["id"]
	except KeyError:
		raise UserError(f"User with username '{USER}' not found.")


def username(UID: str) -> str:
	"""
	Get a users username from their user ID.

	>>> username("zx7gd1yx")
	'1'
	>>> username('7j477kvj')
	'AnInternetTroll'
	>>> username('Sesame Street')
	Traceback (most recent call last):
	    ...
	utils.UserError: User with uid 'Sesame Street' not found.
	"""
	R: dict = requests.get(f"{API}/users/{UID}").json()
	try:
		return R["data"]["names"]["international"]
	except KeyError:
		raise UserError(f"User with uid '{UID}' not found.")


def game(ABR: str) -> tuple[str, str]:
	"""
	Get a games name and game ID from their abbreviation.

	>>> game("mkw")
	('Mario Kart Wii', 'l3dxogdy')
	>>> game("celestep8")
	('CELESTE Classic', '4d7e7z67')
	>>> game("Fake Game")
	Traceback (most recent call last):
	    ...
	utils.GameError: Game with abbreviation 'Fake Game' not found.
	"""
	R: dict = requests.get(f"{API}/games?abbreviation={ABR}").json()
	try:
		GID: str = R["data"][0]["id"]
		GAME: str = R["data"][0]["names"]["international"]
		return (GAME, GID)
	except IndexError:
		raise GameError(f"Game with abbreviation '{ABR}' not found.")


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
	h: float
	m: float

	m, s = divmod(s, 60)
	h, m = divmod(m, 60)
	ms: int = int(round(s % 1 * 1000))

	if not h:
		if not ms:
			return "{}:{:02d}".format(int(m), int(s))
		return "{}:{:02d}.{:03d}".format(int(m), int(s), ms)
	if not ms:
		return "{}:{:02d}:{:02d}".format(int(h), int(m), int(s))
	return "{}:{:02d}:{:02d}.{:03d}".format(int(h), int(m), int(s), ms)
