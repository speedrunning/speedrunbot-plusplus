/* This program gets the number of WRs that a given player (argv[1]) has set. */

#include <stdio.h>
#include <string.h>

#include <curl/curl.h>

#include "utils.h"
#include "wrs.h"

int substr(const char *sub, const char *str, const size_t strl)
{
	int c = 0;
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
	/* Init strings */
	string_t user, runs;
	init_string(&user);
	init_string(&runs);

	/* Get players UID */
	static char uri[URIBUF];
	char uid[UIDBUF];

	snprintf(uri, URIBUF, API "/users?lookup=%s", argv[1]);
	get_req(uri, &user);
	sscanf(user.ptr, "{\"data\":[{\"id\":\"%[^\"]", uid);

	/* Get players PRs */
	snprintf(uri, URIBUF, API "/users/%s/personal-bests?top=1", uid);
	get_req(uri, &runs);

	/* Get counts */
	const int total = substr("\"level\":", runs.ptr, runs.len);
	const int fullgame = substr("\"level\":null", runs.ptr, runs.len);

	printf("%d %d %d\n", fullgame, total - fullgame, total);

	return 0;
}
