#ifndef __VERIFIED_H_
#define __VERIFIED_H_

#define THREAD_COUNT 25

/**
 * @brief Print the commands usage and example if an invalid number of arguments
 * are given.
 */
void usage(void) __attribute__((noreturn));

/**
 * @brief The routine executed by all the threads. It performs a GET request to
 * the sr.c API, and adds the number of runs recieved to the `counts` array.
 * 
 * @param tnum The threads number which can range from 0 to 24. It's a void
 * pointer, but the binary representation is identical to that of an int holding
 * the threads number.
 * @return void* NULL.
 */
void *routine(void *tnum);

#endif /* !__VERIFIED_H_ */
