/* This program gets the number of WRs that a given player (argv[1]) has set. */

#include <stdio.h>
#include <stdlib.h>

#include "srcom/utils.h"
#include "srcom/worldrecords.h"

void usage(void)
{
	fputs("Usage: `+worldrecords [PLAYER NAME]`\n"
	      "Example: `+worldrecords AnInternetTroll`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

int main(int argc, char **argv)
{
	if (argc != 2)
		usage();

	char *uid = get_uid(argv[1]);
	if (!uid) {
		fprintf(stderr, "Error: User with username '%s' not found.\n",
		        argv[1]);
		return EXIT_FAILURE;
	}

	string_t runs;
	init_string(&runs);

	/* Get players PRs. */
	static char uri[URIBUF];
	snprintf(uri, URIBUF, API "/users/%s/personal-bests?top=1", uid);
	get_req(uri, &runs);

	/*
	 * Each run will have a level. If the level is null, the run is a
	 * fullgame run. Counting the number of "levels" is a quick and easy way
	 * to get the number of runs without the need of parsing the JSON.
	 */
	const unsigned int total = count_substr(runs.ptr,
	                                        "\"level\":", TOTAL_KEY_LEN);
	const unsigned int fullgame = count_substr(runs.ptr, "\"level\":null",
	                                           LEVEL_KEY_LEN);

	printf("Full Game: %u\n"
	       "Individual Level: %u\n"
	       "Total: %u\n",
	       fullgame, total - fullgame, total);
	return EXIT_SUCCESS;
}
