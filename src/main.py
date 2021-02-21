#!/usr/bin/env python3.9

import json

from bot import DATA, SRBpp


def check_jsons():
    CONFIG = f"{DATA}/config.json"
    try:
        f = open(CONFIG, "r")
    except FileNotFoundError:
        token = input("BOT SETUP - Enter bot token: ")
        with open(CONFIG, "w+") as f:
            json.dump({"token": token}, f, indent=4)


def run_bot():
    bot = SRBpp()
    bot.run()


if __name__ == "__main__":
    check_jsons()
    run_bot()
