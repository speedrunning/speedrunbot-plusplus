/*
 * Get all the given categories for a given game (argv[1]). This includes
 * fullgame, miscellaneous, and individual level categories.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <jansson.h>

#include "defines.h"
#include "srcom/categories.h"
#include "srcom/utils.h"

void usage(void)
{
	fputs("Usage: `+categories [GAME]`\n"
	      "Example: `+categories mkw`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

bool get_categories(json_t *root, struct counts_t *counts,
                    struct names_t *names, string_t *json)
{
	json_t *data;
	root = json_loads(json->ptr, 0, NULL);
	if (!root) {
		fputs("Error: Unable to parse sr.c reponse, try again later.\n",
		      stderr);
		exit(EXIT_FAILURE);
	}

	data = json_object_get(root, "data");
	size_t num_cats = json_array_size(data);
	if (num_cats == 0) { /* No categories. */
		json_decref(root);
		return false;
	}

	names->fullgame = safe_malloc(num_cats * sizeof(char *));
	names->il = safe_malloc(num_cats * sizeof(char *));
	names->misc = safe_malloc(num_cats * sizeof(char *));

	for (size_t i = 0; i < num_cats; i++) {
		json_t *obj, *type, *misc, *name;
		obj = json_array_get(data, i);
		misc = json_object_get(obj, "miscellaneous");
		name = json_object_get(obj, "name");

		/* Update the counters. */
		if (misc->type == JSON_TRUE) {
			names->misc[counts->misc++] =
			        (char *) json_string_value(name);
		} else {
			type = json_object_get(obj, "type");
			if (json_string_length(type) == 8) /* "per-game" */
				names->fullgame[counts->fullgame++] =
				        (char *) json_string_value(name);
			else
				names->il[counts->il++] =
				        (char *) json_string_value(name);
		}
	}

	return true;
}

int main(int argc, char **argv)
{
	if (argc != 2)
		usage();

	string_t game, categories;
	init_string(&game);
	init_string(&categories);

	/* Get the games ID and name. */
	char gid[UIDBUF], gname[BUFSIZ], uri[URIBUF];
	snprintf(uri, URIBUF, API "/games?abbreviation=%s", argv[1]);
	get_req(uri, &game);

	sscanf(game.ptr,
	       "{\"data\":[{\"id\":\"%[^\"]\",\"names\":{\"international\":\"%["
	       "^\"]",
	       gid, gname);
	if (*gid == '\0') {
		fprintf(stderr,
		        "Error: Game with abbreviation '%s' not found.\n",
		        argv[1]);
		return EXIT_FAILURE;
	}

	snprintf(uri, URIBUF, API "/games/%s/categories", gid);
	get_req(uri, &categories);

	/*
	 * We initialize the root here so that we can print the category names
	 * before doing `json_decref()` which could cause many issues.
	 */
	json_t *root = NULL;
	struct counts_t counts = {.fullgame = 0, .il = 0, .misc = 0};
	struct names_t names = {.fullgame = NULL, .il = NULL, .misc = NULL};
	printf("Categories - %s\n", gname);

	if (!get_categories(root, &counts, &names, &categories)) {
		printf("No categories\n");
		return EXIT_SUCCESS;
	}

	/*
	 * This looks super slow, but I've been informed that it isn't due to
	 * input buffering. I hope that person was right.
	 */
	if (counts.fullgame > 0) {
		printf("Fullgame: %s", names.fullgame[0]);
		for (unsigned int i = 1; i < counts.fullgame; i++)
			printf(", %s", names.fullgame[i]);
		puts("");
	}
	if (counts.il > 0) {
		printf("Individual Level: %s", names.il[0]);
		for (unsigned int i = 1; i < counts.il; i++)
			printf(", %s", names.il[i]);
		puts("");
	}
	if (counts.misc > 0) {
		printf("Miscellaneous: %s", names.misc[0]);
		for (unsigned int i = 1; i < counts.misc; i++)
			printf(", %s", names.misc[i]);
		puts("");
	}

	json_decref(root);
	return EXIT_SUCCESS;
}
