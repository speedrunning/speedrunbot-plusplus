#ifndef __DEFINES_H_
#define __DEFINES_H_

/* Supress unused parameter warnings. */
#ifdef __GNUC__
#	define UNUSED(x) UNUSED_##x __attribute__((__unused__))
#else
#	define UNUSED(x) UNUSED_##x
#endif

/* For when I haven't included <stdlib.h>. */
#ifndef EXIT_SUCCESS
#	define EXIT_SUCCESS 0
#	define EXIT_FAILURE 1
#endif

/* Took this from stackoverflow. */
#define STR_HELPER(x) #x
#define STR(x)        STR_HELPER(x)

/* The maximum number of runs that can be returned from the sr.c API. */
#define MAX_RECV      200
#define MAX_RECV_BULK 1000

/* Maximum length of a speedrun.com username */
#define SRC_MAX_USERNAME 30

/* The length of a speedrun.com ID */
#define ID_LEN 8

#endif /* !__DEFINES_H_ */
