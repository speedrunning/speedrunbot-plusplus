#ifndef __RUNQUEUE_H_
#define __RUNQUEUE_H_

#define SIZE_KEY     "\"size\":"
#define KEY_LEN      7
#define THREAD_COUNT 5
/*
 * strlen(API "/runs?game=&status=new&max=" STR(MAX_RECV) "&offset=") + ID_LEN + 1 + strlen("10000")
 */
#define URIBUF 83

#endif /* !__RUNQUEUE_H_ */
