#!/usr/bin/env python3.9

"""
This program gets the current World Record for a given game (argv[1]) and
optionally a specific category (argv[2]) and subcategories (argv[3..]).
"""

from sys import argv, exit

import requests
from utils import *

# Get the game ID and name
r: dict = requests.get(f"{API}/games?abbreviation={argv[1]}").json()
GID: str = r["data"][0]["id"]
GAME: str = r["data"][0]["names"]["international"]

# Get the games categories
r = requests.get(f"{API}/games/{GID}/categories").json()
CAT: str
cid: str = None

try:
    CAT = argv[2]
    for c in r["data"]:
        if c["name"] == CAT:
            cid = c["id"]
            break
# Get default category if none supplied
except IndexError:
    for c in r["data"]:
        if c["type"] == "per-game":
            CAT = c["name"]
            cid = c["id"]
            break

# TODO: Support levels
if not cid:
    exit(0)

# Get WR
r = requests.get(f"{API}/leaderboards/{GID}/category/{cid}?top=1").json()

# TODO: Coop support
TIME: str = r["run"]["times"]["primary_t"]
PLAYER: str = username(r["run"]["players"][0]["id"])

# TODO: Get the video link
print(f"World Record: {GAME} - {CAT}\n" + f"```{TIME}  {PLAYER}```")
