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
	"""
	Extract the float value of the video timestamp from the given JSON.

	>>> convert('{"cmt": "1.234"}')
	1.234
	"""
	TIME: float
	# JSON files have { so safe to assume it can be loaded
	if "{" in DATA:
		TIME = float(loads(DATA)["cmt"])
	else:
		TIME = float(DATA)
	return TIME


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


def _retime(START_TIME: float, END_TIME: float, FRAMERATE: int) -> str:
	"""
	Calculate the total duration of the run from the video endpoints and
	framerate.

	>>> _retime(23.692, 69.184, 30)
	'Mod Note: Retimed (Start Frame: 710, End Frame: 2075, FPS: 30, Total Time: 0:45.500)'
	>>> _retime(0, 2.534, 60)
	'Mod Note: Retimed (Start Frame: 0, End Frame: 152, FPS: 60, Total Time: 0:02.533)'
	"""
	FRAMES: Union[int, float] = (
		(floor(END_TIME * FRAMERATE) / FRAMERATE)
		- (floor(START_TIME * FRAMERATE) / FRAMERATE)
	) * FRAMERATE

	SECONDS: float = round(FRAMES / FRAMERATE * 1000) / 1000

	START_FRAME: int = trunc(START_TIME * FRAMERATE)
	END_FRAME: int = trunc(END_TIME * FRAMERATE)

	TIME: str = ptime(SECONDS)

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
