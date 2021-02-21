#!/usr/bin/env python3.9

from sys import argv

import requests
from utils import *

GAME: str = argv[1]

# Get default category if none supplied
r: dict = requests.get(f"{API}/games/{GAME}/categories").json()
CAT: str = r["data"][0]["id"]

r = requests.get(f"{API}/leaderboards/{GAME}/category/{CAT}?top=10").json()
print(
    "\n".join(
        [
            f"{run['place']} {username(run['run']['players'][0]['id'])} {ptime(run['run']['times']['primary_t'])}"
            for run in r["data"]["runs"]
        ]
    )
)
