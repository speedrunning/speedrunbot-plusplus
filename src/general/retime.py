#!/usr/bin/env python3.9

from json import loads
from math import floor, trunc
from sys import argv, exit, stderr
from typing import Literal, Union

EXIT_SUCCESS: Literal[0] = 0
EXIT_FAILURE: Literal[1] = 1


def usage() -> None:
	"""
	Print the commands usage and example if an invalid number of arguments
	are given.
	"""
	print(
		"Usage: `+retime [FRAMERATE] [STARTING_FRAME (Optional)]`\n"
		+ 'Example: `+retime 30 \'{ "cmt": "16.200" }\' \'{ "cmt": "16.200" }\'`'
	)
	exit(EXIT_FAILURE)

def convert(DATA: str) -> float:
	TIME: float
	# JSON files have { so safe to assume it can be loaded
	if "{" in DATA:
		TIME = float(loads(DATA)["cmt"])
	else:
		TIME = float(DATA)
	return TIME


def time_format(TIME: float) -> str:
	HOURS: int = floor(TIME / 3600)
	MINUTES: int = floor((TIME % 3600) / 60)
	SECONDS: float = TIME % 60
	retime: str = ""

	if HOURS > 0:
		retime += f"{HOURS}:{'0' if MINUTES < 10 else ''}"
	retime += f"{MINUTES}:{'0' if SECONDS < 10 else ''}{round(SECONDS, 3)}"
	return retime


def _retime(START_TIME: float, END_TIME: float, FRAMERATE: int) -> str:
	FRAMES: Union[int, float] = (
		(floor(END_TIME * FRAMERATE) / FRAMERATE)
		- (floor(START_TIME * FRAMERATE) / FRAMERATE)
	) * FRAMERATE

	SECONDS: float = round(FRAMES / FRAMERATE * 1000) / 1000

	START_FRAME: int = trunc(START_TIME * FRAMERATE)
	END_FRAME: int = trunc(END_TIME * FRAMERATE)

	TIME: str = time_format(SECONDS)

	return f"Mod Note: Retimed (Start Frame: {START_FRAME}, End Frame: {END_FRAME}, FPS: {FRAMERATE}, Total Time: {TIME})"


def main() -> int:
	FRAMERATE: str
	START_TIME: str
	END_TIME: str

	if len(argv) != 4:
		usage()
		exit(EXIT_SUCCESS)
	else:
		_, FRAMERATE, START_TIME, END_TIME = argv
		try:
			print(
				_retime(
					FRAMERATE=int(FRAMERATE),
					START_TIME=convert(START_TIME),
					END_TIME=convert(END_TIME),
				)
			)
		except Exception as e:
			print(e)
			exit(EXIT_FAILURE)
		return EXIT_SUCCESS


if __name__ == "__main__":
	RET: int = main()
	exit(RET)
