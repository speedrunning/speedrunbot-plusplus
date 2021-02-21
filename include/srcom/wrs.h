#ifndef __WRS_H_
#define __WRS_H_

#include <stddef.h>

/**
 * @brief Find the number of occurances of a substring in a string.
 * 
 * @param sub The substring to search for.
 * @param str The string to seach through.
 * @param strl The length of the string to search through.
 * @return int The number of occurances.
 */
int substr(const char *const sub, const char *const str, const size_t strl);

#endif /* !__WRS_H_ */