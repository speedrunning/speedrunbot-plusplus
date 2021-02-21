#!/usr/bin/env python3.9

"""
This program gets the number of WRs that a given player (argv[1]) has set.
"""

from sys import argv

import requests
from utils import *

UID: str = uid(argv[1])
r: dict = requests.get(f"{API}/users/{UID}/personal-bests?top=1").json()

fullgame: int = 0
il: int = 0

for run in r["data"]:
    if run["run"]["level"]:
        il += 1
    else:
        fullgame += 1

print(f"{fullgame} {il} {fullgame + il}")
