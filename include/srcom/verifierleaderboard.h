#ifndef __VERIFIERLEADERBOARD_H_
#define __VERIFIERLEADERBOARD_H_

#define CMDBUF (16 + SRC_MAX_USERNAME * 2)
#define MODBUF 128

struct mod_t {
	char name[SRC_MAX_USERNAME];
	int examined;
};

struct data_t {
	char cmd[CMDBUF];
	struct mod_t *mod;
};

/**
 * @brief Print the commands usage and example if an invalid number of arguments
 * are given.
 */
void usage(void) __attribute__((noreturn));

/**
 * @brief Get the length of an integer up to 6 digits.
 *
 * @param n The number whos length you want to get.
 * @return int The length of the integer.
 */
int ilen(const int n);

/**
 * @brief A helper function passed to qsort(3) to sort moderators.
 *
 * @param v1 The first mod to compare.
 * @param v2 The second mod to compare.
 * @return int The difference in examined runs between v1 and v2.
 */
int sort(const void *v1, const void *v2);

/**
 * @brief The routine executed by all the threads. It calls the `./verified`
 * program in order to get the amount of runs each moderator has examined.
 *
 * @param data A data_t struct containing the threads mod_t to work with, and
 * the command to execute.
 * @return void* NULL.
 */
void *routine(void *data);

/**
 * @brief Get the number of runs all the mods have examined.
 *
 * @param mods An array of mod_t structs.
 * @param argv An array of commandline arguments.
 */
void get_verified(struct mod_t *mods, char **argv);

/**
 * @brief Add a mod to the mods array.
 *
 * @param name The mods name.
 * @param mod The mods array.
 */
void add_mod(char *name, struct mod_t *mod);

/**
 * @brief Get all of a games mods.
 *
 * @param game The name of the game.
 * @param mods_array The array of mods.
 */
void get_mods(char *game, struct mod_t *mods_array);

/**
 * @brief Check if the arguments passed to the program are valid.
 *
 * @param argc The number of commandline arguments.
 * @param argv An array of commandline arguments.
 */
void check_args(int argc, char **argv);

#endif /* __VERIFIERLEADERBOARD_H_ */
