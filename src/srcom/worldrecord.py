#!/usr/bin/env python3.9

"""
This program gets the current world record for a given game (argv[1]) and
optionally a specific category (argv[2]) and subcategories (argv[3..]).
"""

from sys import argv, exit

import requests
from utils import *


def main() -> int:
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
        return EXIT_FAILURE

    # Get WR
    r = requests.get(f"{API}/leaderboards/{GID}/category/{cid}?top=1").json()

    # TODO: Strip flags from guests name
    # Example: "[br][nl]Mango Man" -> "Mango Man"
    WR: dict = r["data"]["runs"][0]["run"]
    TIME: str = ptime(WR["times"]["primary_t"])
    PLAYERS: str = ", ".join(
        username(player["id"]) if player["rel"] == "user" else player["name"]
        for player in WR["players"]
    )
    VIDEOS: list[dict[str, str]] = WR["videos"]["links"]

    print(
        f"World Record: {GAME} - {CAT}\n"
        + f"{TIME}  {PLAYERS}\n"
        + "\n".join(f"<{R['uri']}>" for R in VIDEOS)
    )
    return EXIT_SUCCESS


if __name__ == "__main__":
    ret: int = main()
    exit(ret)
