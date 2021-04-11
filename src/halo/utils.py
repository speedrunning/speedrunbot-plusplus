#!/usr/bin/env python3.9

"""
This file contains all sorts of variables and utilities used in the halo
related programs.
"""

from json import loads

API: str = "https://haloruns.com/api"

EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1


class Run:
	def __init__(self, data) -> None:
		if type(data) == str:
			data = loads(data)
		self.id: int = data["id"]
		self.run_time: int = data["run_time"]
		self.timestamp: int = data["timestamp"]
		self.vid: str = data["vid"]
		self.is_coop: bool = data["is_coop"]
		self.time: str = data["time"]
		self.game_name: str = data["game_name"]
		self.level_name: str = data["level_name"]
		self.difficulty_name: str = data["difficulty_name"]
		self.runners: list[str] = data["runners"]
		self.points: int = data["points"]
