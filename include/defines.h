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

/* The maximum number of runs that can be returned from the sr.c API. */
#define MAX_RECV 200

#endif /* !__DEFINES_H_ */
