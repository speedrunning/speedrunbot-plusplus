# SpeedrunBot++

SpeedrunBot++ aims to be an upgrade from the effectively abandoned yet popular
[SpeedrunBot](https://github.com/Slush0Puppy/speedrunbot). The bot is still in
it's early stages, but the plan is to support a variety of speedrunning sites
such as The Mario Kart Players' Page, Authoritative Minesweeper, etc.

## Inner Workings

Unlike the typical structure of having a bot written in Python, which contains
the implementations of each command, here the bot is merely a bridge between the
discord user and a variety of small programs that do one thing and do it well.
For example, when a user runs the command to get a speedrun.com users total run
count, the bot runs the program located at `src/srcom/bin/runs` as a subprocess.

Since every command is it's own little program, you can use any language you'd
like to write a command so long as you can get an executable out of it. That
being said, some extremely basic commands like `+source` (links this repository)
are just built into the bot for performance reasons.

## Running the Bot

To run the bot, you will need to be on a unix based OS, sorry Windows users. The
bot it only tested on debian-based Linux, but it can be made to work on other
systems with minimal effort.

To install the required dependencies and build the programs, you need to run the
setup script. The script will require superuser privileges and will search for
sudo and doas in your `PATH`. If neither is found, you will be prompted to enter
the name of the command that grants you superuser privileges.

```sh
$ ./setup.sh
Checking for program to grant superuser privileges
Checking for C compiler
Checking for Python3.9
Installing dependencies
Building executables
$
```

The script will also check to make sure you have a C compiler and python
installed. Python3.9 is recommended and it is not guaranteed that anything will
work on other versions of Python3. Additionally, if you use a C compiler that
is not `clang` or `gcc` (why?), you want to make sure that `cc` links to it, or
you can just edit the setup script yourself.

In the case that you do NOT have Python3.9 installed, the script will prompt you
asking if you would like to install Python3.9.

```sh
$ ./setup.sh
Checking for a program to grant superuser privileges
Checking for C compiler
Checking for Python3.9
ERROR: Python3 was not found. The bot will not work. You can either install Python3 from your distributions package manager or you can install Python3.9 from this script.
Do you want to install python3.9? (Only tested on Debian) [y/N]: y
...  # Python3.9 installation output
$
```

## Developer Information

### File Structure

```sh
.
├── data          # Configuration files and related.
├── include       # C preprocessor include files.
│   └── srcom     # Include files for speedrun.com.
└── src           # Source code files.
    ├── cogs      # The bots cogs.
    └── srcom     # Command source code files for speedrun.com.
        ├── bin   # Program executables and binaries.
        └── objs  # C compiler object files.
```
