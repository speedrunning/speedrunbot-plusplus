#ifndef __UTILS_H_
#define __UTILS_H_

#include <stddef.h>

#define API    "https://www.speedrun.com/api/v1"
#define UIDBUF 16
#define URIBUF 128

/* Supress unused parameter warnings */
#ifdef __GNUC__
#	define UNUSED(x) UNUSED_##x __attribute__((__unused__))
#else
#	define UNUSED(x) UNUSED_##x
#endif

/* For when I haven't included <stdlib.h> */
#ifndef EXIT_SUCCESS
#	define EXIT_SUCCESS 0
#	define EXIT_FAILURE 1
#endif

/**
 * @brief A struct representing a string. This makes working with libcurl a bit
 * easier.
 */
typedef struct {
	char *ptr;
	size_t len;
} string_t;

/**
 * @brief Initialize a string_t struct.
 * 
 * @param str A pointer to the string_t struct to initialize.
 */
void init_string(string_t *str);

/**
 * @brief Get a players user ID.
 * 
 * @param username The players speedrun.com username.
 * @return char* The players user ID.
 */
char *get_uid(const char *const username);

/**
 * @brief Perform a GET request to the speedrun.com API and store the result.
 * 
 * @param uri The URI to make a request to.
 * @param json A pointer to the string_t struct where the contents of the JSON
 * will be stored.
 */
void get_req(const char *uri, string_t *json);

/**
 * @brief Read the incoming bytes from curl into `json`.
 * 
 * @param ptr A pointer to the delivered data.
 * @param size This is always 1.
 * @param nmemb Number of bytes recieved.
 * @param json pointer to the string_t struct where the json will be stored.
 * @return size_t The number of bytes taken care of.
 */
size_t write_callback(const void *ptr, const size_t size, const size_t nmemb,
                      string_t *json);

/**
 * @brief Find the number of occurances of a substring in a string.
 * 
 * @param sub The substring to search for.
 * @param str The string to seach through.
 * @param strl The length of the string to search through.
 * @return unsigned int The number of occurances.
 */
unsigned int substr(const char *const sub, const char *const str,
                    const size_t strl);

#endif /* !__UTILS_H_ */