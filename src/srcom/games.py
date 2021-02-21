#!/usr/bin/env python3.9

"""
This program gets the number of games that a given player (argv[1]) has submit
runs to.
"""

from sys import argv

import requests
from utils import *

UID: str = uid(argv[1])
r: dict = requests.get(f"{API}/users/{UID}/personal-bests").json()

count: int = 0
played: list = []
for run in r["data"]:
    if (game := run["run"]["game"]) not in played:
        count += 1
        played.append(game)

print(count)
