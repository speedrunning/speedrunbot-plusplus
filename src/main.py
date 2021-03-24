#!/usr/bin/env python3.9

from os.path import isfile

from bot import ROOT_DIR, SRBpp


def check_files() -> None:
	"""
	Make sure all required files are present.
	"""
	TOKEN_FILE: str = f"{ROOT_DIR}/token"
	if not isfile(TOKEN_FILE):
		TOKEN: str = input("BOT SETUP - Enter bot token: ")
		with open(TOKEN_FILE, "w+") as f:
			f.write(TOKEN)


def _start() -> None:
	check_files()
	BOT: SRBpp = SRBpp()
	BOT.run()


if __name__ == "__main__":
	_start()
