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
char unique[8196][UIDBUF];

void usage(void)
{
#ifdef CATEGORIES
	fputs("Usage: `+categoriesplayed [PLAYER NAME]`\n"
	      "Example: `+categoriesplayed AnInternetTroll`\n",
	      stderr);
#else
	fputs("Usage: `+games [PLAYER NAME]`\n"
	      "Example: `+games AnInternetTroll`\n",
	      stderr);
#endif
	exit(EXIT_FAILURE);
}

bool in_unique(char *id)
{
	int i = 0;
	for (; unique[i][0] != '\0'; i++)
		if (strcmp(unique[i], id) == 0)
			return true;

	strncpy(unique[i], id, UIDBUF);
	return false;
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

	string_t prs;
	init_string(&prs);

	/* Get players' PRs. */
	char uri[URIBUF];
	snprintf(uri, URIBUF, API "/users/%s/personal-bests", uid);
	get_req(uri, &prs);

	/* We don't free `prs.ptr` after this because it's slow. */
	json_t *root, *data;
	json_error_t error;
	root = json_loads(prs.ptr, 0, &error);
	if (!root) {
		fputs("Error: Unable to parse sr.c reponse, try again later.\n",
		      stderr);
		return EXIT_FAILURE;
	}

	/* Loop through PRs and find number of unique games. */
	unsigned int c = 0;
	data = json_object_get(root, "data");
	for (size_t i = 0, len = json_array_size(data); i < len; i++) {
		json_t *obj, *run, *id;
		obj = json_array_get(data, i);
		run = json_object_get(obj, "run");
#ifdef CATEGORIES
		id = json_object_get(run, "category");
#else
		id = json_object_get(run, "game");
#endif

		/* Typecast to discard 'const' qualifier. */
		char *id_str = (char *) json_string_value(id);
		if (!in_unique(id_str))
			c++;
	}

	json_decref(root);
#ifdef CATEGORIES
	printf("Categories: %u\n", c);
#else
	printf("Games: %u\n", c);
#endif
	return EXIT_SUCCESS;
}
