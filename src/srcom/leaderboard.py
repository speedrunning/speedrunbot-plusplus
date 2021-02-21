#!/usr/bin/env python3.9

"""
This program returns the top 10 for a given gave (argv[1]) as well as an
optional category (argv[2]) and optional subcategory (argv[3]).
"""

from sys import argv

import requests
from utils import *

r: dict = requests.get(f"{API}/games?abbreviation={argv[1]}").json()
GID: str = r["data"][0]["id"]
GAME: str = r["data"][0]["names"]["international"]

# Get default category if none supplied
r = requests.get(f"{API}/games/{GID}/categories").json()
CAT: str = r["data"][0]["id"]

r = requests.get(f"{API}/leaderboards/{GID}/category/{CAT}?top=10").json()

rows: list[list[str]] = [
    [
        str(run["place"]),
        ptime(run["run"]["times"]["primary_t"]),
        username(run["run"]["players"][0]["id"]),
    ]
    for run in r["data"]["runs"]
]

MAXLEN: int = max([len(i[1]) for i in rows])

print(
    GAME
    + "\n"
    + "\n".join(
        [
            f"{row[0].rjust(2).ljust(3)} {row[1].ljust(MAXLEN + 1)} {row[2]}"
            for row in rows
        ]
    )
)