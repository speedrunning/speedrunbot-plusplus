/* This program runs all the Makefiles in the `src/` directory. */

#include <sys/types.h>
#include <sys/wait.h>

#include <dirent.h>
#include <errno.h>
#include <libgen.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "admin/compile.h"
#include "defines.h"

/* These directories are excluded by the program. */
const char *const MAKE_EXCLUDES[] = {".", "..", "__pycache__", "cogs", NULL};

bool in_excludes(const char *dname)
{
	for (int i = 0; MAKE_EXCLUDES[i] != NULL; i++)
		if (strcmp(dname, MAKE_EXCLUDES[i]) == 0)
			return true;
	return false;
}

void make(const char *dname)
{
	pid_t pid = fork();
	switch (pid) {
	case -1:
		perror("fork");
		exit(EXIT_FAILURE);
	case 0:
		execlp("make", "make", "-C", dname, CC, NULL);
		perror("execlp");
		exit(EXIT_FAILURE);
	default:
		if ((pid = wait(NULL)) == -1) {
			perror("wait");
			exit(EXIT_FAILURE);
		}
	}
}

int main(int UNUSED(argc), char **argv)
{
	/*
	 * Since this will only be run by people that know what they're doing,
	 * it's fine to just print out the actual error messages as opposed to
	 * something less scary to the average user.
	 */
	if (chdir(dirname(argv[0])) == -1) {
		perror("chdir");
		return EXIT_FAILURE;
	}
	if (chdir("../../") == -1) {
		perror("chdir");
		return EXIT_FAILURE;
	}

	DIR *dirp = opendir(".");
	if (dirp == NULL) {
		perror("opendir");
		return EXIT_FAILURE;
	}

	/*
	 * Set `errno` to 0 to differenciate between an end of the directory
	 * stream and an error as recommended by `man 3 readdir`.
	 */
	errno = 0;
	struct dirent *entry;
	while ((entry = readdir(dirp)) != NULL) {
		if (entry->d_type != DT_DIR || in_excludes(entry->d_name))
			continue;

		make(entry->d_name);
	}

	if (errno) {
		perror("readdir");
		return EXIT_FAILURE;
	}

	if (closedir(dirp) == -1) {
		perror("closedir");
		return EXIT_FAILURE;
	}
	return EXIT_SUCCESS;
}
