#!/usr/bin/env python3.9

"""
This file contains all sorts of variables and utilities used in the sr.c
related programs.
"""

import requests

API: str = "https://www.speedrun.com/api/v1"


def uid(USER: str) -> str:
    """Get a users user ID from their username."""
    r: dict = requests.get(f"{API}/users/{USER}").json()
    return r["data"]["id"]
