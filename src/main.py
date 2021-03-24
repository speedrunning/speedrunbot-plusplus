#!/usr/bin/env python3.9

import json
from os.path import isfile

from bot import DATA, SRBpp


def check_jsons() -> None:
	"""
	Make sure all JSON configuration files are present.
	"""
	CONFIG: str = f"{DATA}/srbpp.json"
	if not isfile(CONFIG):
		TOKEN: str = input("BOT SETUP - Enter bot token: ")
		with open(CONFIG, "w+") as f:
			json.dump({"token": TOKEN, "botmasters": []}, f, indent=4)


def _start() -> None:
	check_jsons()
	BOT: SRBpp = SRBpp()
	BOT.run()


if __name__ == "__main__":
	_start()
