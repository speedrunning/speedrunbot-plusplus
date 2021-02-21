# SpeedrunBot++

SpeedrunBot++ aims to be an upgrade from the effectively abandoned yet popular SpeedrunBot. The bot is still in it's early stages, but the plan is to support a variety of speedrunning sites such as The Mario Kart Players' Page, Authoritative Minesweeper, etc.

## Inner Workings

Unlike the typical structure of having a bot written in Python, which contains the implementations of each command, here the bot is merely a bridge between the discord user and a variety of small programs that do one thing and do it well. For example, when a user runs the command to get a speedrun.com users total run count, the bot runs the program located at `src/srcom/bin/runs` as a subprocess.

Since every command is it's own little program, you can use any language you'd like to write a command so long as you can get an executable out of it. That being said, some extremely basic commands like `+source` (links this repository) are just built into the bot for performance reasons.
