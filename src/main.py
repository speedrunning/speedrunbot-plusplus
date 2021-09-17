#!/usr/bin/env python3.9

from os.path import isfile

from bot import ROOT_DIR, SRBpp

TOKEN_FILE = f"{ROOT_DIR}/token"


def check_files() -> None:
	"""
	Make sure all required files are present.
	"""
	if not isfile(TOKEN_FILE):
		token = input("BOT SETUP - Enter bot token: ")
		with open(TOKEN_FILE, "w+", encoding="utf-8") as f:
			f.write(token)


def _start() -> None:
	"""
	The genesis function.
	"""
	check_files()
	bot = SRBpp()
	bot.run()


if __name__ == "__main__":
	_start()
