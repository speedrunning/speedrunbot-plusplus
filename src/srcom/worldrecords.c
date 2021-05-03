/*
 * This program gets the number of WRs that a given player (argv[1]) has set. Optionally, a game
 * (argv[2]) can be specified.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "srcom/utils.h"
#include "srcom/worldrecords.h"

static void
usage(void)
{
	fputs("Usage: `+worldrecords [PLAYER NAME] [GAME (OPTIONAL)]`\n"
	      "Example: `+worldrecords AnInternetTroll mkw`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

int
main(int argc, char **argv)
{
	if (argc == 1)
		usage();

	char *uid = get_uid(argv[1]);
	if (!uid) {
		fprintf(stderr, "Error: User with username '%s' not found.\n", argv[1]);
		exit(EXIT_FAILURE);
	}

	char uri[URIBUF];
	struct game_t *game = NULL;
	if (argc > 2 && (game = get_game(argv[2])) == NULL) {
		fprintf(stderr,
			"Error: Game with abbreviation '%s' not found.\n",
			argv[2]);
		exit(EXIT_FAILURE);
	}

	string_t runs;
	init_string(&runs);

	/* Get players PRs. */
	sprintf(uri, API "/users/%s/personal-bests?top=1&game=%s", uid,
	         game ? game->id : "");
	get_req(uri, &runs);

	/*
	 * Each run will have a level. If the level is null, the run is a
	 * fullgame run. Counting the number of "levels" is a quick and easy way
	 * to get the number of runs without the need of parsing the JSON.
	 */
	const unsigned int total = count_substr(runs.ptr, TOTAL_KEY, TOTAL_KEY_LEN);
	const unsigned int fullgame = count_substr(runs.ptr, LEVEL_KEY, LEVEL_KEY_LEN);

	if (argc >= 3)
		printf("World Record Count: %s - %s\n", argv[1], game->name);
	else
		printf("World Record Count: %s\n", argv[1]);

	printf("Full Game: %u\n"
	       "Individual Level: %u\n"
	       "Total: %u\n",
	       fullgame, total - fullgame, total);

#ifdef DEBUG
	free(runs.ptr);
#endif
	return EXIT_SUCCESS;
}
