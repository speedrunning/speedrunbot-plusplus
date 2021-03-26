/*
 * This program gets the number of runs that a given player (argv[1]) has
 * verified or rejected.
 */

#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "defines.h"
#include "srcom/utils.h"
#include "srcom/verified.h"

bool done = false;
char uri_base[URIBUF];
int offset_start = 0;
int counts[THREAD_COUNT] = {0};

void usage(void)
{
	fputs("Usage: `+verified [PLAYER NAME]`\n"
	      "Example: `+verified AnInternetTroll`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

void *routine(void *tnum)
{
	/* 
	 * Equivalant to `(int) tnum` but supresses compiler warnings that can
	 * be safely ignored. 
	 */
	int s, i_tnum = *((int *) &tnum);
	char uri[URIBUF], size[URIBUF];
	string_t json;

	snprintf(uri, URIBUF, "%s%d", uri_base,
	         offset_start + MAX_RECV * i_tnum);
	init_string(&json);
	get_req(uri, &json);

	char *size_key = last_substr(json.ptr, "\"size\":", 7);
	sscanf(size_key, "\"size\":%[^,]", size);

	if ((s = atoi(size)) < MAX_RECV)
		done = true;
	counts[i_tnum] += s;

	free(json.ptr);
	return NULL;
}

int main(int argc, char **argv)
{
	if (argc != 2)
		usage();

	const char *uid = get_uid(argv[1]);
	if (!uid) {
		fprintf(stderr, "Error: User with username '%s' not found.\n",
		        argv[1]);
		return EXIT_FAILURE;
	}
	snprintf(uri_base, URIBUF,
	         API "/runs?examiner=%s&max=200&offset=", uid);

	while (!done) {
		pthread_t threads[THREAD_COUNT];
		for (int i = 0; i < THREAD_COUNT; i++) {
			/*
			* This cast is a could be replaced with a simple `(void *) i`
			* cast, but the compiler doesn't like it when I do that.
			*/
			if (pthread_create(&threads[i], NULL, &routine,
			                   *((void **) &i))
			    != 0) {
				fputs("Error: Failed to create thread.\n",
				      stderr);
				return EXIT_FAILURE;
			}
		}

		for (int i = 0; i < THREAD_COUNT; i++) {
			if (pthread_join(threads[i], NULL) != 0) {
				fputs("Error: Failed to join thread.\n",
				      stderr);
				return EXIT_FAILURE;
			}
		}

		offset_start += THREAD_COUNT * MAX_RECV;
	}

	int total = 0;
	for (int i = 0; i < THREAD_COUNT; i++)
		total += counts[i];
	printf("Verified: %d\n", total);
	return EXIT_SUCCESS;
}
