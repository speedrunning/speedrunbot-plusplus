#!/usr/bin/env python3.9
# vi: ft=python

undefine(len, format, `__file__')

"""
This file contains all sorts of variables and utilities used in the sr.c related programs.
"""

import asyncio
import json
import shlex
from json.decoder import JSONDecodeError
from os.path import dirname
from sys import exit, stderr
from time import sleep
from typing import Any, Literal, NoReturn, Optional, Union
from dataclasses import dataclass

from redis import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from requests import Session
from requests.exceptions import ConnectionError as RequestsConnectionError

API = "https://www.speedrun.com/api/v1"
RATE_LIMIT = 420

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

CACHEDIR = f"{dirname(__file__)}/../../../cache/srcom"

try:
	with open(f"config.json", encoding="utf-8") as f:
		config = json.load(f)
except IOError:
	config = {}

define(`search', `config[$1] if $1 in config else $2')
redis = Redis(host=search("redis_hostname", "localhost"), port=search("redis_port", 6379), db=(search("redis_db", 0)), decode_responses=True)

session = Session()

class User:
	"""
	A super basic class representing a user. If any field of the user is unset (for example
	someone without a profile picture) that field will be set to an empty string.

	Make sure to not be stupid and call the contructor without a name or UID.
	"""
	def __init__(self, name: str = "", uid: str = "") -> None:
		if name:
			data = api_get(f"{API}/users?lookup={name}")["data"][0]
		else:
			data = api_get(f"{API}/users/{uid}")["data"]

		_construct_class(self, data)

def _construct_class(obj: object, data: dict) -> None:
	"""
	Create the class `obj` as described by the dictionary `dict`.
	"""
	for key in data:
		if type(data[key]) == dict:
			setattr(obj, key, type(key, (object,), {}))
			try:
				_construct_class(obj.__getattribute__(key), data[key])
			except TypeError:
				_construct_class(obj.__getattribute__(obj, key), data[key])
		else:
			setattr(obj, key, data[key] if data[key] else "")

def usage(usage: str) -> NoReturn:
	"""
	Print the commands usage and example if an invalid number of arguments are given to stderr.
	"""
	print(usage, file=stderr)
	exit(EXIT_FAILURE)


def error_and_die(e: Union[Exception, str]) -> NoReturn:
	"""
	Print an error message to stderr and then exit.
	"""
	print(f"Error: {e}", file=stderr)
	exit(EXIT_FAILURE)


def api_get(uri: str, params: Optional[dict[str, Any]] = {}) -> dict:
	"""
	This is a wrapper around `requests.get()` that does error checking for status codes.
	"""
	while True:
		try:
			r = session.get(uri, params=params)
		except RequestsConnectionError:
			try:
				data = redis.hget("cache", hash(uri))
			except RedisConnectionError as e:
				error_and_die(e)
			else:
				if data:
					return json.loads(data)
				else:
					sleep(2)
		else:
			if r.ok:
				data = r.json()
				try:
					redis.hset("cache", hash(uri), r.text)
				except RedisConnectionError as e:
					error_and_die(e)
				return data
			if r.status_code == RATE_LIMIT:
				try:
					data = redis.hget("cache", hash(uri))
				except RedisConnectionError:
					error_and_die(e)
				if data:
					return json.loads(data)
				else:
					sleep(5)
			else:
				try:
					error_and_die(r.json()["message"])
				except JSONDecodeError:
					error_and_die("The site is probably down go complain to ELO")


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
	SystemExit: 1
	"""

	r = api_get(f"{API}/users", params={"lookup": user})
	try:
		return r["data"][0]["id"]
	except IndexError:
		error_and_die(f"User with username '{user}' not found.")


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
	SystemExit: 1
	"""
	r = api_get(f"{API}/users/{uid}")
	return r["data"]["names"]["international"]


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
	SystemExit: 1
	"""
	r = api_get(f"{API}/games", params={"abbreviation": abbrev})
	try:
		gid: str = r["data"][0]["id"]
		gname: str = r["data"][0]["names"]["international"]
		return (gname, gid)
	except IndexError:
		error_and_die(f"Game with abbreviation '{abbrev}' not found.")


def subcatid(cid: str, subcat: str, lflag: bool = False) -> tuple[str, str]:
	"""
	Get the subcategory ID and and value ID from the given category ID and subcategory value
	label. Whoever decided to handle subcategories like this should consider switching
	professions.

	>>> subcatid("w20gmyzk", "Random Seed")
	('5ly7759l', '5q804wk1')
	>>> subcatid("wk68zp21", "Skips")
	('j84rwjl9', '81p4xxg1')
	>>> subcatid("xd130359", "Mobile", True)
	('ylqmdmvn', '810enwwq')
	>>> subcatid("mkeoz98d", "Gem Skips")
	Traceback (most recent call last):
		...
	SystemExit: 1
	"""
	r = api_get(f"{API}/{'levels' if lflag else 'categories'}/{cid}/variables")
	lsubcat = subcat.lower()
	try:
		for var in r["data"]:
			if var["is-subcategory"]:
				for v in var["values"]["values"]:
					if var["values"]["values"][v]["label"].lower() == lsubcat:
						return (var["id"], v)
	except KeyError:  # TODO: Test if this is still required after Ziro's PR.
		error_and_die(f"Subcategory with label '{subcat}' not found.")
		# raise NotSupportedError(f"Subcategories are not yet supported for ILs.")
	error_and_die(f"Subcategory with label '{subcat}' not found.")


def ptime(s: float) -> str:
	"""
	Pretty print a time in the format H:M:S.ms. Empty leading fields are disgarded with the
	exception of times under 60 seconds which show 0 minutes.

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
	Get the category ID with the name `CAT` from the request `R`. This function doesn't do the
	request itself, since it's meant to work with both fullgame and IL's, amongst other reasons.

	>>> r = api_get(f"{API}/games/l3dxogdy/categories")
	>>> getcid("Nitro Tracks", r)
	'7kj6mz23'
	>>> getcid("Retro Tracks", r)
	'xk9v3gd0'
	>>> r = api_get(f"{API}/games/l3dxogdy/levels")
	>>> getcid("This game has no levels", r)
	>>> r = api_get(f"{API}/games/4d7e7z67/levels")
	>>> getcid("100m", r)
	'rdn25e5d'
	"""
	lcat = cat.lower()
	for c in r["data"]:
		if c["name"].lower() == lcat:
			return c["id"]
	return None
