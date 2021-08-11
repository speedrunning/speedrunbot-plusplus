# Formatting

Formatting is easy. Just use `format.sh`. It requires `bash(1)` and `GNU unexpand(1)` to work as
well as `isort(1)` and `black(1)` and stuff but you probably have all that already if you're working
on this.

Use snake_case for variables and functions and whatnot. Use CAPS for constants in any language and
`#define`'s in C/C++. Use CAPS for shell script variables.

If a C/C++ function takes no parameters, write it as `type func(void)` instead of `type func()`.

Begin a program with a shebang if appropriate and a comment explaining what the program does, for
example:

```c
/* This program gets the number of games that a given player (argv[1]) has submit runs to. */

#include <stdbool.h>
/* Rest of code */
```

or:

```python
#!/usr/bin/env python3.9

"""This file contains all sorts of variables and utilities used in the sr.c related programs."""

import requests
# Rest of code
```

In Python typehint all your functions. If an argument is optional, mark it as such. If it is a
union, mark it as such, etc. If a function has no return value, typehint that with `-> None:`.

This isn't really "formatting" but do not write cringe code. If you find yourself repeating yourself
often or writing multiple near-identical commands just make use of POSIX `m4` macros. Here is an
example from `games.go` which implements both `+games` and `+categoriesplayed`:

```m4
undefine(len)
changequote(',')

package main

...

type JsonData struct {
	Data []struct {
		Run struct {
			ID string `json:"ifdef('GAMES','game','category')"`
		} `json:"run"`
	} `json:"data"`
}

...

	tree := &BinaryTree{}
	for _, run := range runs.Data {
		tree.insert(run.Run.ID)
	}
	fmt.Printf("ifdef('GAMES','Games','Categories') Played: `%s`\n%d\n", os.Args[1], count)
}
```

In the above example, the file `games.go` is once passed through `m4` and compiled and once passed
through `m4 -DGAMES` and compiled. For more information see either `man 1p m4` or
[this](https://www.ibm.com/docs/en/aix/7.2?topic=concepts-m4-macro-processor-overview) IBM page.
