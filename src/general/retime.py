#!/usr/bin/env python3.9

from json import loads
from math import floor, trunc
from sys import argv, exit, stderr
from typing import Literal, NoReturn

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def usage() -> NoReturn:
	"""
	Print the commands usage and example if an invalid number of arguments are given.
	"""
	print(
		"Usage: `+retime [framerate] [STARTING_FRAME (Optional)]`\n"
		+ 'Example: `+retime 30 \'{ "cmt": "16.200" }\' \'{ "cmt": "16.200" }\'`',
		file=stderr,
	)
	exit(EXIT_FAILURE)


def convert(data: str) -> float:
	"""
	Extract the float value of the video timestamp from the given JSON.

	>>> convert('{"cmt": "1.234"}')
	1.234
	>>> convert('5.295')
	5.295
	"""
	# JSON files have { so safe to assume it can be loaded
	if "{" in data:
		time = float(loads(data)["cmt"])
	else:
		time = float(data)
	return time


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


def _retime(start_time: float, end_time: float, framerate: int) -> str:
	"""
	Calculate the total duration of the run from the video endpoints and framerate.

	>>> _retime(23.692, 69.184, 30)
	'Mod Note: Retimed (Start Frame: 710, End Frame: 2075, FPS: 30, Total Time: 0:45.500)'
	>>> _retime(0, 2.534, 60)
	'Mod Note: Retimed (Start Frame: 0, End Frame: 152, FPS: 60, Total Time: 0:02.533)'
	"""
	frames = (
		(floor(end_time * framerate) / framerate) - (floor(start_time * framerate) / framerate)
	) * framerate

	seconds = round(frames / framerate * 1000) / 1000

	start_frame = trunc(start_time * framerate)
	end_frame = trunc(end_time * framerate)

	time = ptime(seconds)

	return (
		f"Mod Note: Retimed (Start Frame: {start_frame}, End Frame: {end_frame}, FPS: {framerate},"
		f" Total Time: {time})"
	)


def main() -> int:
	if len(argv) != 4:
		usage()

	_, framerate, start_time, end_time = argv
	try:
		print(
			_retime(
				framerate=int(framerate),
				start_time=convert(start_time),
				end_time=convert(end_time),
			)
		)
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(EXIT_FAILURE)
	return EXIT_SUCCESS


if __name__ == "__main__":
	exit(main())
