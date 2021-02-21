#!/usr/bin/env python3.9

"""
This program gets the number of runs that a given player (argv[1]) has set.
"""

from sys import argv

import requests
from utils import *

fullgame: int = 0
il: int = 0

UID: str = uid(argv[1])

offset: int = 0
lastpage: bool = False
while not lastpage:
    r: dict = requests.get(f"{API}/runs?user={UID}&max=200&offset={offset}").json()
    for run in r["data"]:
        if run["level"] is None:
            fullgame += 1
        else:
            il += 1

    offset += 200
    try:
        if r["pagination"]["links"][-1]["rel"] == "prev":
            lastpage = True
    except IndexError:
        lastpage = True


print(f"{fullgame} {il} {fullgame + il}")
