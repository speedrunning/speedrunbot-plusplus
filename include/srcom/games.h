#ifndef __GAMES_H_
#define __GAMES_H_

/**
 * @brief Print the commands usage and example if an invalid number of arguments
 * are given.
 */
void usage(void) __attribute__((noreturn));

/**
 * @brief Check if `id` is in the `unique` array, and if not, add it.
 * 
 * @param id The ID to check for.
 * @return true The ID was in the array.
 * @return false The ID was not in the array.
 */
bool in_unique(char *gid);

#endif /* !__GAMES_H_ */
