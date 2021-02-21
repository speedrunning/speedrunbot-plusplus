CC     := gcc
CFLAGS := -O3 -std=c99 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes -Wno-unused-result
INC    := -I../../include/srcom

cprogs  := bin/wrs bin/games bin/modcount
pyprogs := bin/leaderboard bin/runs bin/worldrecord bin/utils

all: $(cprogs) $(pyprogs)
$(shell mkdir -p bin/ objs/)

# Python programs
bin/%: %.py
	chmod +x $< && cp $< $@

# C programs

# It would be nice if I didn't need to make a new rule for each program, but I
# am not sure how to do so without linking unnessesary libraries in programs
# that don't need them.
bin/wrs: objs/wrs.o objs/utils.o
	$(CC) $(CFLAGS) -o $@ $^ -lcurl

bin/modcount: objs/modcount.o objs/utils.o
	$(CC) $(CFLAGS) -o $@ $^ -lcurl

bin/games: objs/games.o objs/utils.o
	$(CC) $(CFLAGS) -o $@ $^ -lcurl -ljansson

objs/%.o: %.c
	$(CC) $(CFLAGS) $(INC) -o $@ -c $<

# Phony targets
.PHONY: clean
clean:
	rm -rf objs/ bin/
