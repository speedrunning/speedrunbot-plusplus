#!/usr/bin/env python3.9

"""
This program gets the number of games and series that a given player (argv[1])
is a moderator of.
"""

from sys import argv

import requests
from utils import *

UID: str = uid(argv[1])

# Setting _bulk to `yes` increases the game limit from 200 to 1000. But who in
# their right mind would moderate >200 games anyways? Only one that comes to
# mind is April kek.
r: dict = requests.get(f"{API}/games?moderator={UID}&_bulk=yes").json()
GAMES: int = len(r["data"])
r = requests.get(f"{API}/series?moderator={UID}").json()
SERIES: int = len(r["data"])

print(f"{GAMES} {SERIES} {GAMES + SERIES}")
