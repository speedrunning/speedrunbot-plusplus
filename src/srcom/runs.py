#!/usr/bin/env python3.9

"""
This program gets the number of runs that a given player (argv[1]) has set.
"""

from itertools import count
from sys import argv, exit

import requests
from utils import *

fullgame: int = 0
il: int = 0

try:
    UID = uid(argv[1])
except UserError:
    exit(0)

for offset in count(0, 200):
    r: dict = requests.get(
        f"{API}/runs?user={UID}&max=200&offset={offset}"
    ).json()
    for run in r["data"]:
        if run["level"] is None:
            fullgame += 1
        else:
            il += 1

    p: list[dict[str, str]] = r["pagination"]["links"]
    if not p or "next" not in p[-1].values():
        break


print(
    f"Full Game: {fullgame}\n"
    + f"Individual Level: {il}\n"
    + f"Total: {fullgame + il}"
)
