#!/usr/bin/env python3.9

"""
This program gets information for a given user (argv[1])
"""


from datetime import datetime
from getopt import GetoptError, getopt
from sys import argv, exit, stderr
from typing import Literal, Optional

from utils import *

USAGE = "Usage: `+whois [USERNAME]`\n" + "Example: `+whois 1`"


def date_format(date: datetime) -> str:
	last = date.day % 10
	if last == 1:
		return date.strftime("%-dst %B, %Y")
	if last == 2:
		return date.strftime("%-dnd %B, %Y")
	if last == 3:
		return date.strftime("%-drd %B, %Y")
	return date.strftime("%-dth %B, %Y")


def main() -> int:
	try:
		opts, args = getopt(argv[1:], ":u:", ["uid="])
	except GetoptError as e:
		usage(f"{e}\n{USAGE}")

	uid = None
	for o, a in opts:
		if o in ("-u", "--uid"):
			uid = a
			break

	if uid:
		r = api_get(f"{API}/users/{uid}")["data"]
	else:
		try:
			r = api_get(f"{API}/users?lookup={args[0]}")
			# When getting a user with the `lookup` parameter, the `data` field returns
			# an array of length 1 instead of just the data directly.
			r = r["data"][0]
		except IndexError:
			usage(USAGE)

	print(
		f"__THUMBNAIL__: {r['assets']['image']['uri']}\n"
		+ f"**Username**: [{r['names']['international']}]({r['weblink']})"
		+ (f' ({r["names"]["japanese"]})' if r["names"]["japanese"] else "")
		+ f"User ID: {r['id']}\n"
		+ (f"\n**Pronouns**: {r['pronouns']}" if r["pronouns"] else "")
		+ (f"\n**Role**: {r['role'].capitalize()}" if r["role"] != "user" else "")
		+ f"\n**Signed up**: {date_format(datetime.strptime(r['signup'], '%Y-%m-%dT%H:%M:%S%z'))}"
		+ f"\n**Socials**: "
		+ (f"[Twitch]({r['twitch']['uri']}) " if r["twitch"] else "")
		+ (f"[Hitbox]({r['hitbox']['uri']}) " if r["hitbox"] else "")
		+ (f"[Youtube]({r['youtube']['uri']}) " if r["youtube"] else "")
		+ (f"[Twitter]({r['twitter']['uri']}) " if r["twitter"] else "")
		+ (f"[SpeedRunsLive]({r['speedrunslive']['uri']}) " if r["speedrunslive"] else "")
		+ (
			(
				(
					"\n**Region**: "
					+ (
						r["location"]["region"]["names"]["international"]
						+ " "
						+ f'({r["location"]["region"]["code"].upper()})'
						+ (
							f"({r['location']['region']['names']['japanese']})"
							if r["location"]["region"]["names"]["japanese"]
							else ""
						)
					)
				)
				if "region" in r["location"]
				else (
					"\n**Country**: "
					+ r["location"]["country"]["names"]["international"]
					+ " "
					+ f'({r["location"]["country"]["code"].upper()})'
					+ (
						f"({r['location']['country']['names']['japanese']})"
						if r["location"]["country"]["names"]["japanese"]
						else ""
					)
				)
			)
			if r["location"]
			else ""
		)
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
