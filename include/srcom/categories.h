#ifndef __CATEGORIES_H_
#define __CATEGORIES_H_

/* Including because `string_t` is used in a prototype below. */
#include "utils.h"

#define CATLISTBUF 8192

/**
 * @brief A struct containing the counts of each category type.
 */
struct counts_t {
	unsigned int fullgame;
	unsigned int il;
	unsigned int misc;
};

/**
 * @brief A struct containing arrays of strings which store the category names.
 */
struct names_t {
	char *fullgame[CATLISTBUF];
	char *il[CATLISTBUF];
	char *misc[CATLISTBUF];
};

/**
 * @brief Print the commands usage and example if an invalid number of arguments
 * are given.
 */
void usage(void) __attribute__((noreturn));

/**
 * @brief Get all the categories from the given json, and store them by type so
 * that they can be printed out after the function call.
 * 
 * @param root A json_t pointer to the root of the JSON.
 * @param counts The counts_t struct to store the counts of each type of
 * category in.
 * @param names The names_t struct to store the category names in.
 * @param json The JSON containing the category information.
 * @return true Categories were found.
 * @return false The given game has no categories.
 */
bool get_categories(json_t *root, struct counts_t *counts,
                    struct names_t *names, string_t *json);

#endif /* !__CATEGORIES_H_ */
