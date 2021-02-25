#!/usr/bin/env python3.9

"""
This file contains all sorts of variables and utilities used in the sr.c
related programs.
"""

from typing import Union

import requests

API: str = "https://www.speedrun.com/api/v1"


def uid(USER: str) -> Union[str, None]:
    """Get a users user ID from their username. Returns None on error."""
    r: dict = requests.get(f"{API}/users/{USER}").json()
    try:
        return r["data"]["id"]
    except KeyError:
        return None


def username(UID: str) -> str:
    """Get a users username from their user ID."""
    r: dict = requests.get(f"{API}/users/{UID}").json()
    return r["data"]["names"]["international"]


def game(ABR: str) -> tuple[str, str]:
    """Get a games name and game ID from their abbreviation."""
    r: dict = requests.get(f"{API}/games?abbreviation={ABR}").json()
    GID: str = r["data"][0]["id"]
    GAME: str = r["data"][0]["names"]["international"]
    return (GAME, GID)


def ptime(s: float) -> str:
    """
    Pretty print a time in the format H:M:S.ms. Empty leading fields are
    disgarded.
    """
    h: float
    m: float

    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    ms: int = int(s % 1 * 1000)

    if not h:
        if not ms:
            return "{}:{:02d}".format(int(m), int(s))
        return "{}:{:02d}.{:03d}".format(int(m), int(s), ms)
    if not ms:
        return "{}:{:02d}:{:02d}".format(int(h), int(m), int(s))
    return "{}:{:02d}:{:02d}.{:03d}".format(int(h), int(m), int(s), ms)
