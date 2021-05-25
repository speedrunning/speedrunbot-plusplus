#ifndef __UTILS_H_
#define __UTILS_H_

#include <stddef.h>

#include "defines.h"

#define API "https://www.speedrun.com/api/v1"

#ifdef __cplusplus
extern "C" {
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
 * @brief A struct that holds data regarding a game.
 */
struct game_t {
	char id[ID_LEN + 1];
	char name[BUFSIZ];
};

/**
 * @brief A wrapper around `malloc(2)` that does error checking.
 *
 * @param size The amount of bytes to allocate.
 * @return void* A pointer to the allocated memory.
 */
void *xmalloc(const size_t size);

/**
 * @brief A wrapper around `realloc(2)` that does error checking.
 *
 * @param ptr The pointer to reallocate memory to.
 * @param size The amount of bytes to allocate.
 * @return void* A pointer to the reallocated memory.
 */
void *xrealloc(void *ptr, const size_t size);

/**
 * @brief Initialize a string_t struct.
 *
 * @param str A pointer to the string_t struct to initialize.
 */
void init_string(string_t *str);

/**
 * @brief Get a games ID and name from its abbreviation.
 *
 * @param abbrev The games sr.c abbreviation.
 * @return struct game_t* A game_t struct containing game information. If no
 * game was found, NULL will be returned.
 */
struct game_t *get_game(const char *abbrev);

/**
 * @brief Get a players user ID.
 *
 * @param username The players speedrun.com username.
 * @return char* The players user ID, or NULL on error.
 */
char *get_uid(const char *username);

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
size_t write_callback(const void *ptr, const size_t size, const size_t nmemb, string_t *json);

/**
 * @brief Find the number of occurances of a substring in a string.
 *
 * @param str The string to seach through.
 * @param sub The substring to search for.
 * @param subl The length of the substring.
 * @return unsigned int The number of occurances.
 */
unsigned int count_substr(const char *str, const char *const sub, const int subl);

/**
 * @brief Find the last occurance of a substring in a string.
 *
 * @param str The string to seach through.
 * @param sub The substring to search for.
 * @param subl The length of the substring.
 * @return char* A pointer to the last substring found, or NULL if none found.
 */
const char *last_substr(const char *str, const char *const sub, const int subl);

#ifdef __cplusplus
}
#endif

#endif /* !__UTILS_H_ */
