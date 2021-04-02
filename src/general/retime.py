#!/usr/bin/env python3.9

from json import loads
from math import floor, trunc
from sys import argv, exit, stderr
from typing import Literal

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


def main() -> int:
	if len(argv) != 4:
		usage()
		exit(EXIT_SUCCESS)
	else:
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
			print(e)
			exit(EXIT_FAILURE)
		exit(EXIT_SUCCESS)


def convert(data: str) -> float:
	time: float
	# JSON files have { so safe to assume it can be loaded
	if "{" in data:
		time = float(loads(data)["cmt"])
	else:
		time = float(data)
	return time


def time_format(time: float) -> str:
	hours = floor(time / 3600)
	minutes = floor((time % 3600) / 60)
	seconds = time % 60
	retime = ""

	if hours > 0:
		retime += f"{hours}:{'0' if minutes < 10 else ''}"
	retime += f"{minutes}:{'0' if seconds < 10 else ''}{round(seconds, 3)}"
	return retime


def _retime(start_time: float, end_time: float, framerate: int) -> str:
	frames = (
		(floor(end_time * framerate) / framerate)
		- (floor(start_time * framerate) / framerate)
	) * framerate

	seconds = round(frames / framerate * 1000) / 1000

	start_frame = trunc(start_time * framerate)
	end_frame = trunc(end_time * framerate)

	start_time = trunc(start_frame / framerate)
	end_time = trunc(end_frame / framerate)

	time = time_format(seconds)

	return f"Mod Note: Retimed (Start Frame: {start_frame}, End Frame: {end_frame}, FPS: {framerate}, Total Time: {time}"


if __name__ == "__main__":
	main()
