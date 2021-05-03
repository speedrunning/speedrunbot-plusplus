#ifndef __RUNS_H_
#define __RUNS_H_

#define THREAD_COUNT 5
#define SIZE_KEY     "\"size\":"
#define KEY_LEN      7

/*
 * strlen(API "/runs?user=&game=&max=" STR(MAX_RECV) "&offset=" + ID_LEN * 2 + 1 + strlen("100000")
 */
#define URIBUF 87

#endif /* !__RUNQUEUE_H_ */
