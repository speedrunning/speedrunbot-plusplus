#!/usr/bin/env python3.9

import json
from typing import IO

from bot import DATA, SRBpp


def check_jsons() -> None:
	"""
	Make sure all JSON configuration files are present.
	"""
	CONFIG: str = f"{DATA}/config.json"
	try:
		f: IO = open(CONFIG, "r")
	except FileNotFoundError:
		TOKEN: str = input("BOT SETUP - Enter bot token: ")
		with open(CONFIG, "w+") as f:
			json.dump({"token": TOKEN}, f, indent=4)


def main() -> None:
	check_jsons()
	BOT: SRBpp = SRBpp()
	BOT.run()


if __name__ == "__main__":
	main()
