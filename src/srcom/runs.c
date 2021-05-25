/*
 * This program gets the number of runs submit by a player (argv[1]). Optionally
 * a game (argv[2]) can be specified.
 */

#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <jansson.h>

#include "defines.h"
#include "srcom/runs.h"
#include "srcom/utils.h"

bool done = false;
char uri_base[URIBUF];
int offset_start = 0;
int fgcounts[THREAD_COUNT], ilcounts[THREAD_COUNT];

static void
usage(void)
{
	fputs("Usage: `+runs [PLAYER NAME] [GAME (Optional)]`\n"
	      "Example: `+runs AnInternetTroll mkw`\n",
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
	char uri[URIBUF];
	string_t json;

	/* Make a GET request. */
	sprintf(uri, "%s%d", uri_base, offset_start + MAX_RECV * i_tnum);
	init_string(&json);
	get_req(uri, &json);

	const char *size_key = last_substr(json.ptr, SIZE_KEY, KEY_LEN);
	sscanf(size_key, SIZE_KEY "%d", &size);

	if (size < MAX_RECV)
		done = true;

	/* Loop through each pending run and tally the fullgame and IL runs. */
	json_t *root, *data, *obj, *level;
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

int
main(int argc, char **argv)
{
	if (argc == 1)
		usage();

	char *uid;
	struct game_t *game = NULL;

	/* Get the users ID and name. */
	if ((uid = get_uid(argv[1])) == NULL) {
		fprintf(stderr, "Error: User with name '%s' not found.\n", argv[1]);
		exit(EXIT_FAILURE);
	}
	if (argc > 2 && (game = get_game(argv[2])) == NULL) {
		fprintf(stderr, "Error: Game with abbreviation '%s' not found.\n", argv[2]);
		exit(EXIT_FAILURE);
	}

	sprintf(uri_base, API "/runs?user=%s&game=%s&max=" STR(MAX_RECV) "&offset=", uid,
	        game ? game->id : "");

	while (!done) {
		pthread_t threads[THREAD_COUNT];
		for (int i = 0; i < THREAD_COUNT; i++) {
			/*
			 * This cast is a could be replaced with a simple `(void *) i`
			 * cast, but the compiler doesn't like it when I do that.
			 */
			if (pthread_create(&threads[i], NULL, &routine, *((void **) &i)) != 0) {
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

	int fullgame = 0, il = 0;
	for (int i = 0; i < THREAD_COUNT; i++) {
		fullgame += fgcounts[i];
		il += ilcounts[i];
	}

	if (game)
		printf("Run Count: %s - %s\n", argv[1], game->name);
	else
		printf("Run Count: %s\n", argv[1]);

#ifdef DEBUG
	free(game);
#endif

	printf("Fullgame: %d\n"
	       "Individual Level: %d\n"
	       "Total: %d\n",
	       fullgame, il, fullgame + il);

	return EXIT_SUCCESS;
}
