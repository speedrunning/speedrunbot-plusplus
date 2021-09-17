#!/usr/bin/env python3.9

"""
This program gets information for a given user (argv[1])
"""


from datetime import datetime
from getopt import GetoptError, getopt
from sys import argv, exit, stderr
from typing import Literal, Optional

from utils import *

USAGE = "Usage: `+whois src [USERNAME]`\n" + "Example: `+whois src 1`"


def contains(obj: object, attribute: str) -> bool:
	try:
		obj.__getattribute__(obj, attribute)
		return True
	except AttributeError:
		return False


def date_format(date: str) -> str:
	date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
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
		user = User(id=uid)
	else:
		try:
			user = User(name=args[0])
		except IndexError:
			usage(USAGE)

	print(
		(f"__THUMBNAIL__: {user.assets.image.uri}\n" if user.assets.image.uri else "")
		+ f"**Username**: [{user.names.international}]({user.weblink})\n"
		+ (f" ({user.names.japanese})" if user.names.japanese else "")
		+ f"**User ID**: {user.id}"
		+ (f"\n**Pronouns**: {user.pronouns}" if user.pronouns else "")
		+ (f"\n**Role**: {user.role.capitalize()}" if user.role != "user" else "")
		+ f"\n**Signed up**: {date_format(user.signup)}"
		+ f"\n**Socials**: "
		+ (f"[Twitch]({user.twitch.uri}) " if user.twitch else "")
		+ (f"[Hitbox]({user.hitbox.uri}) " if user.hitbox else "")
		+ (f"[Youtube]({user.youtube.uri}) " if user.youtube else "")
		+ (f"[Twitter]({user.twitter.uri}) " if user.twitter else "")
		+ (f"[SpeedRunsLive]({user.speedrunslive.uri}) " if user.speedrunslive else "")
		+ (
			(
				(
					"\n**Region**: "
					+ (
						user.location.region.names.international
						+ " "
						+ f"({user.location.region.code.upper()})"
						+ (
							f"({user.location.region.names.japanese})"
							if user.location.region.names.japanese
							else ""
						)
					)
				)
				if contains(user.location, "region")
				else (
					f"\n**Country**: {user.location.country.names.international} "
					+ f"({user.location.country.code.upper()})"
					+ (
						f"({user.location.country.names.japanese})"
						if user.location.country.names.japanese
						else ""
					)
				)
			)
			if user.location
			else ""
		)
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
