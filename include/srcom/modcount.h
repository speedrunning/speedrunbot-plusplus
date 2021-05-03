#ifndef __MODCOUNT_H_
#define __MODCOUNT_H_

#define ID_KEY  "\"id\":"
#define KEY_LEN 5

/* strlen(API "/games?moderator=&_bulk=yes&max=" STR(MAX_RECV_BULK)) + ID_LEN + 1 */
#define URIBUF 76

#endif /* !__MODCOUNT_H_ */
