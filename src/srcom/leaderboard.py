#!/usr/bin/env python3.9

"""
This program returns the top 10 for a given gave (argv[1]) as well as an
optional category (argv[2]) and optional subcategory (argv[3]).
"""

from sys import argv, exit

import requests
from utils import *


def pad(TIME: str, MS: bool) -> str:
    """
    Pad a time with blank spaces if it doesnt contain milliseconds for output
    formatting.

    >>> pad("59:54.397", True)
    '59:54.397'
    >>> pad("3:42", True)
    '3:42    '
    >>> pad("1:39", False)
    '1:39'
    """
    if not MS:
        return TIME
    return f"{TIME}    " if "." not in TIME else TIME


def main() -> int:
    # Get the games categories
    GAME, GID = game(argv[1])
    r: dict = requests.get(f"{API}/games/{GID}/categories").json()
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

    # Get top 10
    r = requests.get(f"{API}/leaderboards/{GID}/category/{cid}?top=10").json()

    # Set this flag if no runs have milliseconds.
    MS: bool = "." in "".join(
        [ptime(run["run"]["times"]["primary_t"]) for run in r["data"]["runs"]]
    )

    # TODO: Strip flags from guests name
    # Example: "[br][nl]Mango Man" -> "Mango Man"
    rows: list[list[str]] = [
        [
            str(run["place"]),
            pad(ptime(run["run"]["times"]["primary_t"]), MS),
            ", ".join(
                username(player["id"])
                if player["rel"] == "user"
                else player["name"]
                for player in run["run"]["players"]
            ),
        ]
        for run in r["data"]["runs"]
    ]

    # Length of the longest run time, used for output padding
    MAXLEN: int = max([len(i[1]) for i in rows])

    print(
        f"Top {len(rows)}: {GAME} - {CAT}\n"
        + "```"
        + "\n".join(
            [
                f"{row[0].rjust(2).ljust(3)} {row[1].rjust(MAXLEN).ljust(MAXLEN + 1)} {row[2]}"
                for row in rows
            ]
        )
        + "```"
    )
    return EXIT_SUCCESS


if __name__ == "__main__":
    ret: int = main()
    exit(ret)
