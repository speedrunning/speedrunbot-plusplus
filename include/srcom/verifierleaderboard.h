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

#endif /* __VERIFIERLEADERBOARD_H_ */
