/*
 * This program gets the number of runs verified and rejected by a given user
 * (argv[1]) and optionally limits the count to runs from 1 or 2 given games
 * (argv[2] and argv[3]).
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <curl/curl.h>

#include "defines.h"
#include "srcom/utils.h"
#include "srcom/verified.h"

static void
usage(void)
{
	fputs("Usage: `+verified [PLAYER NAME] [GAME (Optional)] [GAME (Optional)]`\n"
	      "Example: `+verified AnInternetTroll mkw mkwextracategories`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

static unsigned int
count_examined(bool *done, string_t *json)
{
	char *ptr = json->ptr;
	unsigned int count = 0, tmp;

	while ((ptr = strstr(ptr + KEY_LEN, SIZE_KEY)) != NULL) {
		sscanf(ptr, SIZE_KEY "%u", &tmp);

		if (tmp < MAX_RECV)
			*done = true;
		count += tmp;
	}

	return count;
}

static void
perform_requests(char *uri_base, unsigned int offset, string_t *json)
{
	char uri[URIBUF];
	int running = 0, numfds;
	CURLcode mc;
	CURL *handles[REQUEST_COUNT];
	CURLM *mhandle;

	if ((mhandle = curl_multi_init()) == NULL) {
		fputs("Error: Unable to initialize curl multi handle.", stderr);
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < REQUEST_COUNT; i++) {
		if ((handles[i] = curl_easy_init()) == NULL) {
			fputs("Error: Unable to initialize curl handle.\n",
			      stderr);
			exit(EXIT_FAILURE);
		}

		sprintf(uri, "%s%u", uri_base, offset);
		offset += MAX_RECV;

		/* Load the contents of the API request to `json`. */
		curl_easy_setopt(handles[i], CURLOPT_URL, uri);
		curl_easy_setopt(handles[i], CURLOPT_WRITEFUNCTION,
		                 write_callback);
		curl_easy_setopt(handles[i], CURLOPT_WRITEDATA, json);
		curl_easy_setopt(handles[i], CURLOPT_FAILONERROR, 1L);

		curl_multi_add_handle(mhandle, handles[i]);
	}

	do {
		mc = curl_multi_perform(mhandle, &running);
		if (mc == CURLM_OK)
			mc = curl_multi_poll(mhandle, NULL, 0, 1000, &numfds);
		else {
			fprintf(stderr,
			        "Error: curl_multi_perform failed, code %d.\n",
			        mc);
			exit(EXIT_FAILURE);
		}

		if (mc != CURLM_OK) {
			fprintf(stderr, "Error: curl_multi failed, code %d.\n",
			        mc);
			exit(EXIT_FAILURE);
		}
	} while (running);

	/* Cleanup */
	curl_multi_cleanup(mhandle);
	for (int i = 0; i < REQUEST_COUNT; i++)
		curl_easy_cleanup(handles[i]);
}

static unsigned int
get_examined(const char *uid, const char *gname)
{
	bool done = false;
	char uri_base[URIBUF];
	unsigned int examined = 0, offset = 0;
	string_t json;
	struct game_t *game = NULL;

	if (gname && (game = get_game(gname)) == NULL) {
		fprintf(stderr,
		        "Error: Game with abbreviation '%s' not found.\n",
		        gname);
		exit(EXIT_FAILURE);
	}

	sprintf(uri_base, API "/runs?examiner=%s&game=%s&max=" STR(MAX_RECV) "&offset=",
	         uid, game ? game->id : "");

	/* Every loop `json` is cleared */
	while (!done) {
		init_string(&json);

		perform_requests(uri_base, offset, &json);
		examined += count_examined(&done, &json);
		offset += MAX_RECV * REQUEST_COUNT;

		free(json.ptr);
	}

	return examined;
}

int
main(int argc, char **argv)
{
	if (argc < 2)
		usage();

	char *uid;
	unsigned int examined;

	if ((uid = get_uid(argv[1])) == NULL) {
		fprintf(stderr, "Error: User with username '%s' not found.\n",
		        argv[1]);
		exit(EXIT_FAILURE);
	}

	examined = get_examined(uid, argv[2]);
	/* Check for the case where the same game is given twice */
	if (argc > 3 && strcmp(argv[2], argv[3]) != 0)
		examined += get_examined(uid, argv[3]);

	printf("Verified: %u\n", examined);
	return EXIT_SUCCESS;
}
