/*
 * This program gets the number of runs in the verification queue of a given game
 * (argv[1]) and optionally a second (argv[2])
 */

#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <jansson.h>

#include "defines.h"
#include "srcom/runqueue.h"
#include "srcom/utils.h"

bool done;
char uri_base[URIBUF];
int offset_start;
int fgcounts[THREAD_COUNT], ilcounts[THREAD_COUNT];

static void
usage(void)
{
	fputs("Usage: `+runqueue [GAME] [GAME (Optional)]`\n"
	      "Example: `+runqueue mkw mkwextracategories`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

static void *
routine(void *tnum)
{
	/*
	 * Equivalant to `(int) tnum` but supresses compiler warnings that can
	 * be safely ignored.
	 */
	int size, i_tnum = *((int *) &tnum);
	const char *size_key;
	char uri[URIBUF];
	string_t json;
	json_t *root, *data, *obj, *level;

	/* Make a GET request. */
	sprintf(uri, "%s%d", uri_base, offset_start + MAX_RECV * i_tnum);
	init_string(&json);
	get_req(uri, &json);

	size_key = last_substr(json.ptr, SIZE_KEY, KEY_LEN);
	sscanf(size_key, SIZE_KEY "%d", &size);

	if (size < MAX_RECV)
		done = true;

	/* Loop through each pending run and tally the fullgame and IL runs. */
	root = json_loads(json.ptr, 0, NULL);
	if (!root) {
		fputs("Error: Unable to parse sr.c reponse, try again later.\n", stderr);
		exit(EXIT_FAILURE);
	}
	data = json_object_get(root, "data");

	for (size_t i = 0, len = json_array_size(data); i < len; i++) {
		obj = json_array_get(data, i);
		level = json_object_get(obj, "level");

		if (level->type != JSON_NULL)
			ilcounts[i_tnum]++;
		else
			fgcounts[i_tnum]++;
	}

	json_decref(root);
	free(json.ptr);
	return NULL;
}

static void
runqueue(const struct game_t *game)
{
	string_t json;
	init_string(&json);

	sprintf(uri_base, API "/runs?game=%s&status=new&max=" STR(MAX_RECV) "&offset=", game->id);
	done = false;
	offset_start = 0;
	while (!done) {
		pthread_t threads[THREAD_COUNT];
		for (int i = 0; i < THREAD_COUNT; i++) {
			if (pthread_create(&threads[i], NULL, &routine, (void *) i) != 0) {
				fputs("Error: Failed to create thread.\n", stderr);
				exit(EXIT_FAILURE);
			}
		}

		for (int i = 0; i < THREAD_COUNT; i++) {
			if (pthread_join(threads[i], NULL) != 0) {
				fputs("Error: Failed to join thread.\n", stderr);
				exit(EXIT_FAILURE);
			}
		}

		offset_start += THREAD_COUNT * MAX_RECV;
	}

	free(json.ptr);
}

static void
check_args(int argc, char **argv)
{
	if (argc < 2 || argc > 3)
		usage();

	if (argc == 3 && strcmp(argv[1], argv[2]) == 0) {
		fputs("Error: The same game cannot be provided twice.\n", stderr);
		exit(EXIT_FAILURE);
	}
}

int
main(int argc, char **argv)
{
	const bool two_games = (argc == 3);
	unsigned int fullgame = 0, il = 0;
	struct game_t *games[2] = {0};

	check_args(argc, argv);

	for (int i = 1; i < argc; i++) {
		if ((games[i - 1] = get_game(argv[i])) == NULL) {
			fprintf(stderr, "Error: Game with abbreviation '%s' not found.\n", argv[i]);
			exit(EXIT_FAILURE);
		}
	}

	for (int i = 1; i < argc; i++)
		runqueue(games[i - 1]);

	for (int i = 0; i < THREAD_COUNT; i++) {
		fullgame += fgcounts[i];
		il += ilcounts[i];
	}

	printf("Runs Awaiting Verification: `%s`", games[0]->name);
	if (two_games)
		printf(" and `%s`", games[1]->name);
	putchar('\n');

#ifdef DEBUG
	free(games[0]);
	free(games[1]);
#endif

	printf("Fullgame: %u\n"
	       "Individual Level: %u\n"
	       "Total: %u\n",
	       fullgame, il, fullgame + il);
	return EXIT_SUCCESS;
}
