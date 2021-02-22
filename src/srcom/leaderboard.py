#!/usr/bin/env python3.9

"""
This program returns the top 10 for a given gave (argv[1]) as well as an
optional category (argv[2]) and optional subcategory (argv[3]).
"""

from sys import argv, exit

import requests
from utils import *


def pad(time: str) -> str:
    """
    Pad a time with blank spaces if it doesnt contain milliseconds for output
    formatting.
    """
    return f"{time}    " if "." not in time else time


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

# Get top 10
r = requests.get(f"{API}/leaderboards/{GID}/category/{cid}?top=10").json()

rows: list[list[str]] = [
    [
        str(run["place"]),
        pad(ptime(run["run"]["times"]["primary_t"])),
        username(run["run"]["players"][0]["id"]),
    ]
    for run in r["data"]["runs"]
]

# Length of the longest run time, used for output padding
MAXLEN: int = max([len(i[1]) for i in rows])

print(
    f"{GAME} - {CAT}"
    + "\n"
    + "\n".join(
        [
            f"{row[0].rjust(2).ljust(3)} {row[1].rjust(MAXLEN).ljust(MAXLEN + 1)} {row[2]}"
            for row in rows
        ]
    )
)
