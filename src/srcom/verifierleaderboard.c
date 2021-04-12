/*
 * This program outputs a leaderboard of all moderators for a given game
 * (argv[1]) and optionally a given second game (argv[2]). The mods are ranked
 * based on how many runs they have examined.
 */

#include <libgen.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <jansson.h>

#include "defines.h"
#include "srcom/utils.h"
#include "srcom/verifierleaderboard.h"

int num_mods = 0, max_name = 0;

void usage(void)
{
	fputs("Usage: `+verifierleaderboard [GAME] [GAME (Optional)]`\n"
	      "Example: `+verifierleaderboard mkw mkwextracategories`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

int ilen(const int n)
{
	if (n >= 100000)
		return 6;
	if (n >= 10000)
		return 5;
	if (n >= 1000)
		return 4;
	if (n >= 100)
		return 3;
	if (n >= 10)
		return 2;
	return 1;
}

int sort(const void *v1, const void *v2)
{
	struct mod_t m1 = *(struct mod_t *) v1;
	struct mod_t m2 = *(struct mod_t *) v2;

	return m2.examined - m1.examined;
}

void *routine(void *vdata)
{
	FILE *fp;
	struct data_t *data = (struct data_t *) vdata;

	if ((fp = popen(data->cmd, "r")) == NULL) {
		fputs("Error: Failed to open pipe", stderr);
		exit(EXIT_FAILURE);
	}

	fscanf(fp, "Verified: %d", &data->mod->examined);

	if (pclose(fp) == -1) {
		fputs("Error: Failed to close pipe", stderr);
		exit(EXIT_FAILURE);
	}

	return NULL;
}

void get_verified(struct mod_t *mods, char **argv)
{
	struct data_t data[num_mods];
	pthread_t threads[num_mods];

	argv++;
	for (int i = 0; i < num_mods; i++, mods++) {
		/* Construct data to send to thread. */
		data[i].mod = mods;
		snprintf(data[i].cmd, CMDBUF, "./verified %s %s %s", mods->name,
		         *argv, *(argv + 1) ? *(argv + 1) : "");

		if (pthread_create(&threads[i], NULL, &routine, &data[i])
		    != 0) {
			fputs("Error: Failed to create thread\n", stderr);
			exit(EXIT_FAILURE);
		}
	}

	for (int i = 0; i < num_mods; i++) {
		if (pthread_join(threads[i], NULL) != 0) {
			fputs("Error: Failed to join thread\n", stderr);
			exit(EXIT_FAILURE);
		}
	}
}

void add_mod(char *name, struct mod_t *mod)
{
	size_t len;

	/* If a mods name matches, return. If not add them in at the end */
	for (int i = 0; i < MODBUF; i++, mod++) {
		if (*(mod->name) == '\0') {
			if ((len = strlen(name)) > (size_t) max_name)
				max_name = len;

			strcpy(mod->name, name);
			num_mods++;
			return;
		}

		if (strcmp(mod->name, name) == 0)
			return;
	}
}

void get_mods(char *game, struct mod_t *mods_array)
{
	char uri[URIBUF];
	string_t json;
	json_t *root, *data, *obj, *mods;
	json_t *mdata, *mobj, *mname, *mnameint;

	/* Get JSON containing all moderators. */
	init_string(&json);
	snprintf(uri, URIBUF, API "/games?abbreviation=%s&embed=moderators",
	         game);
	get_req(uri, &json);

	/* Ugly jansson JSON parsing. */
	root = json_loads(json.ptr, 0, NULL);
	if (!root) {
		fputs("Error: Unable to parse sr.c reponse, try again later.\n",
		      stderr);
		exit(EXIT_FAILURE);
	}

	data = json_object_get(root, "data");
	obj = json_array_get(data, 0);
	mods = json_object_get(obj, "moderators");
	mdata = json_object_get(mods, "data");

	/* For each moderator, get their "international" name. */
	for (size_t i = 0, len = json_array_size(mdata); i < len; i++) {
		mobj = json_array_get(mdata, i);
		mname = json_object_get(mobj, "names");
		mnameint = json_object_get(mname, "international");

		/* Cast to remove const qualifier. */
		add_mod((char *) json_string_value(mnameint), mods_array);
	}

	json_decref(root);
	free(json.ptr);
}

void check_args(int argc, char **argv)
{
	argv++;
	if (argc == 1)
		usage();

	if (argc > 3) {
		fputs("Error: Too many games given, you can give a maximum of "
		      "2.\n",
		      stderr);
		exit(EXIT_FAILURE);
	}

	if (argc == 3 && strcmp(*argv, *(argv + 1)) == 0) {
		fputs("Error: You cannot provide the same game twice.\n",
		      stderr);
		exit(EXIT_FAILURE);
	}
}

int main(int argc, char **argv)
{
	check_args(argc, argv);
	struct mod_t mods[MODBUF] = {0};

	for (int i = 1; i < argc; i++)
		get_mods(argv[i], mods);

	if (num_mods == 0) {
		printf("```No mods for any game found```");
		return EXIT_SUCCESS;
	}

	/*
	 * Change into the programs directory so that can call ./verified with a
	 * relative path.
	 */
	if (chdir(dirname(argv[0])) == -1) {
		fputs("Error: Unable to change current directory", stderr);
		exit(EXIT_FAILURE);
	}

	get_verified(mods, argv);
	qsort(mods, num_mods, sizeof(struct mod_t), sort);

	int max_len = ilen(mods[0].examined);
	puts("```");
	for (int i = 0; i < num_mods; i++)
		printf("%*d   %-*s %*d\n", 2, i + 1, max_name + 1, mods[i].name,
		       max_len, mods[i].examined);
	puts("```");

	return EXIT_SUCCESS;
}
