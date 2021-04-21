#ifndef __VERIFIERLEADERBOARD_H_
#define __VERIFIERLEADERBOARD_H_

#define CMDBUF 256
#define MODBUF 128

struct mod_t {
	char name[SRC_MAX_USERNAME];
	int examined;
};

struct data_t {
	char cmd[CMDBUF];
	int index;
	struct mod_t *mods;
};

#endif /* __VERIFIERLEADERBOARD_H_ */
