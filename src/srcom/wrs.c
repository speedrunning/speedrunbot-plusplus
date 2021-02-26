/* This program gets the number of WRs that a given player (argv[1]) has set. */

#include <stdio.h>

#include "utils.h"

int main(int UNUSED(argc), char **argv)
{
	char *uid = get_uid(argv[1]);

	string_t runs;
	init_string(&runs);

	/* Get players PRs */
	static char uri[URIBUF];
	snprintf(uri, URIBUF, API "/users/%s/personal-bests?top=1", uid);
	get_req(uri, &runs);

	/*
	 * Each run will have a level. If the level is null, the run is a
	 * fullgame one. Counting the number of "levels" is a quick and easy way
	 * to get the number of runs without the need of parsing the JSON.
	 */
	const unsigned int total = substr(runs.ptr, "\"level\":", 8);
	const unsigned int fullgame = substr(runs.ptr, "\"level\":null", 12);

	printf("Full Game: %u\n"
	       "Individual Level: %u\n"
	       "Total: %u\n",
	       fullgame, total - fullgame, total);
	return EXIT_SUCCESS;
}
