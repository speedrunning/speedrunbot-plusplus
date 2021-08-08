#!/usr/bin/env python3.9

"""
This program gets information for a given user (argv[1])
"""

from argparse import ArgumentParser
from datetime import datetime
from sys import exit, stderr
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
	parser = ArgumentParser()
	parser.add_argument("--uid", type=str, help="A speedrun.com user ID", default=None)
	parser.add_argument("username", type=str, help="A speedrun.com username", nargs="?", default=None)
	args = parser.parse_args()

	if not args.username and not args.uid:
		usage(USAGE)

	if not args.uid:
		uid = getuid(args.username)
	else:
		uid = args.uid

	# Get the games categories.
	r = api_get(f"{API}/users/{uid}")

	print(
		f"**Username**: "
		+ f"[{r['data']['names']['international']}]({r['data']['weblink']})"
		+ (f' ({r["data"]["names"]["japanese"]})' if r["data"]["names"]["japanese"] else "")
		+ (f"\n**Pronouns**: {r['data']['pronouns']}" if r["data"]["pronouns"] else "")
		+ (f"\n**Role**: {r['data']['role'].capitalize()}" if r["data"]["role"] != "user" else "")
		+ f"\n**Signed up**: {date_format(datetime.strptime(r['data']['signup'], '%Y-%m-%dT%H:%M:%S%z'))}"
		+ f"\n**Socials**: "
		+ (f"[Twitch]({r['data']['twitch']['uri']}) " if r["data"]["twitch"] else "")
		+ (f"[Hitbox]({r['data']['hitbox']['uri']}) " if r["data"]["hitbox"] else "")
		+ (f"[Youtube]({r['data']['youtube']['uri']}) " if r["data"]["youtube"] else "")
		+ (f"[Twitter]({r['data']['twitter']['uri']}) " if r["data"]["twitter"] else "")
		+ (
			f"[SpeedRunsLive]({r['data']['speedrunslive']['uri']}) "
			if r["data"]["speedrunslive"]
			else ""
		)
		+ (
			(
				(
					"\n**Region**: "
					+ (
						r["data"]["location"]["region"]["names"]["international"]
						+ " "
						+ f'({r["data"]["location"]["region"]["code"]})'
						+ (
							f"({r['data']['location']['region']['names']['japanese']})"
							if r["data"]["location"]["region"]["names"]["japanese"]
							else ""
						)
					)
				)
				if "region" in r["data"]["location"]
				else (
					"\n**Country**: "
					+ r["data"]["location"]["country"]["names"]["international"]
					+ " "
					+ f'({r["data"]["location"]["country"]["code"]})'
					+ (
						f"({r['data']['location']['country']['names']['japanese']})"
						if r["data"]["location"]["country"]["names"]["japanese"]
						else ""
					)
				)
			)
			if r["data"]["location"]
			else ""
		)
	)
	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
