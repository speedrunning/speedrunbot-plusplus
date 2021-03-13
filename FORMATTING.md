# Formatting

Formatting is easy.

If using Python, format with `black -l 80` and imports with `isort`, if using C/C++, format with `clang-format`. When in doubt, run `./format.sh`.

Use snake_case for variables and functions and whatnot. Use CAPS for constants in Python and `#define`'s in C/C++.

If a C/C++ function takes no parameters, write it as `type func(void)` instead of `type func()`.

Use tabs. Even with `black`. `unexpand -t 4 --first-only file.py > file2.py` is your best friend.

Begin a program with a shebang if appropriate and a comment explaining what the program does, for example:

(`games.c`)

```c
/*
 * This program gets the number of games that a given player (argv[1]) has
 * submit runs to.
 */

#include <stdbool.h>
/* Rest of code */
```

(`utils.py`)

```python
#!/usr/bin/env python3.9

"""
This file contains all sorts of variables and utilities used in the sr.c
related programs.
"""

import requests
# Rest of code
```
