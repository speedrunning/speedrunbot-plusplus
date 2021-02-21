/* This program gets the number of WRs that a given player (argv[1]) has set. */

#include <stdio.h>
#include <string.h>

#include "utils.h"
#include "wrs.h"

unsigned int substr(const char *const sub, const char *const str,
                    const size_t strl)
{
	unsigned int c = 0;
	const size_t subl = strlen(sub);

	for (size_t i = 0; i < strl - subl; i++) {
		if (strstr(str + i, sub) == str + i) {
			c++;
			i += subl - 1;
		}
	}

	return c;
}

int main(int UNUSED(argc), char **argv)
{
	char *uid = get_uid(argv[1]);

	string_t runs;
	init_string(&runs);

	/* Get players PRs */
	static char uri[URIBUF];
	snprintf(uri, URIBUF, API "/users/%s/personal-bests?top=1", uid);
	get_req(uri, &runs);

	const unsigned int total = substr("\"level\":", runs.ptr, runs.len);
	const unsigned int fullgame = substr("\"level\":null", runs.ptr,
	                                     runs.len);

	printf("%u %u %u\n", fullgame, total - fullgame, total);

	return EXIT_SUCCESS;
}
