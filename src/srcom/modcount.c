/*
 * This program gets the number of games and series that a given player
 * (argv[1]) is a moderator of.
 */

#include <stdio.h>
#include <stdlib.h>

#include "defines.h"
#include "srcom/modcount.h"
#include "srcom/utils.h"

static void usage(void)
{
	fputs("Usage: `+modcount [PLAYER NAME]`\n"
	      "Example: `+modcount AnInternetTroll`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

int main(int argc, char **argv)
{
	if (argc != 2)
		usage();

	char *uid = get_uid(argv[1]);
	if (!uid) {
		fprintf(stderr, "Error: User with username '%s' not found.\n",
		        argv[1]);
		exit(EXIT_FAILURE);
	}

	string_t games, series;
	init_string(&games);
	init_string(&series);

	/*
	 * Setting _bulk to `yes` increases the game limit from 200 to 1000. But
	 * who in their right mind would moderate >200 games anyways? Only one
	 * that comes to mind is April.
	 */
	char uri[URIBUF];
	snprintf(uri, URIBUF,
	         API "/games?moderator=%s&_bulk=yes&max=" STR(MAX_RECV_BULK),
	         uid);
	get_req(uri, &games);
	snprintf(uri, URIBUF, API "/series?moderator=%s&max=" STR(MAX_RECV),
	         uid);
	get_req(uri, &series);

	/*
	 * Each game/series will have an id, so counting the number of IDs is a
	 * quick and easy way to get the number of games/series without the need
	 * of parsing the JSON.
	 */
	const unsigned int gcount = count_substr(games.ptr, ID_KEY, KEY_LEN);
	const unsigned int scount = count_substr(series.ptr, ID_KEY, KEY_LEN);

	printf("Games: %u\n"
	       "Series: %u\n"
	       "Total: %u\n",
	       gcount, scount, gcount + scount);
	return EXIT_SUCCESS;
}
