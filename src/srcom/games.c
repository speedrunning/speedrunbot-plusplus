/*
 * This program gets the number of games that a given player (argv[1]) has
 * submit runs to.
 */

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#include <jansson.h>

#include "games.h"
#include "utils.h"

/* Who in their right mind would play this many games? Besides Cytruss. */
char games[8196][UIDBUF];

bool in_games(char *gid)
{
	int i = 0;
	while (games[i][0] != '\0') {
		if (strcmp(games[i], gid) == 0)
			return true;
		i++;
	}

	strncpy(games[i], gid, UIDBUF);
	return false;
}

int main(int UNUSED(argc), char **argv)
{
	char *uid = get_uid(argv[1]);
	string_t prs;
	init_string(&prs);

	/* Get players' PRs */
	char uri[URIBUF];
	snprintf(uri, URIBUF, API "/users/%s/personal-bests", uid);
	get_req(uri, &prs);

	/* We don't free `prs.ptr` after this because it's slow */
	json_t *root, *data;
	json_error_t error;
	root = json_loads(prs.ptr, 0, &error);
	if (!root)
		return EXIT_FAILURE;

	/* Loop through PRs and find number of unique games */
	unsigned int c = 0;
	data = json_object_get(root, "data");
	for (size_t i = 0, len = json_array_size(data); i < len; i++) {
		json_t *obj, *run, *gid;
		obj = json_array_get(data, i);
		run = json_object_get(obj, "run");
		gid = json_object_get(run, "game");

		/* Typecast to discard 'const' qualifier */
		char *gid_str = (char *) json_string_value(gid);
		if (!in_games(gid_str))
			c++;
	}

	json_decref(root);
	printf("%u\n", c);
	return EXIT_SUCCESS;
}