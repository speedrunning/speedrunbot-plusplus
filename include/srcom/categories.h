#ifndef __CATEGORIES_H_
#define __CATEGORIES_H_

/* Including because `string_t` is used in a prototype below. */
#include "utils.h"

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
	char **fullgame;
	char **il;
	char **misc;
};

#endif /* !__CATEGORIES_H_ */
