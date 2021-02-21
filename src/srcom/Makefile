CC     := gcc
CFLAGS := -O3 -std=c99 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes -Wno-unused-result
INC    := -I../../include/srcom

progs := wrs games

all: $(progs)

wrs: objs/wrs.o objs/utils.o
	@mkdir -p bin/
	$(CC) $(CFLAGS) -o bin/$@ $^ -lcurl

games: objs/games.o objs/utils.o
	@mkdir -p bin/
	$(CC) $(CFLAGS) -o bin/$@ $^ -lcurl -ljansson

objs/%.o: %.c
	@mkdir -p objs/
	$(CC) $(CFLAGS) $(INC) -o $@ -c $<

.PHONY: clean
clean:
	rm -rf objs/ bin/
