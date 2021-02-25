CC     := cc
CFLAGS := -O3 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes -Wno-unused-result
INC    := -I../../include/srcom
PY     := python3.9

cprogs  := bin/wrs bin/games bin/modcount
pyprogs := bin/leaderboard bin/runs bin/worldrecord bin/categories bin/utils.py

all: $(pyprogs) $(cprogs)
$(shell mkdir -p bin/ objs/)

# Python programs
bin/%: %.py
	chmod +x $< && cp $< $@

# This needs to retain the file extension for importability
bin/utils.py: utils.py
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
.PHONY: clean test
clean:
	rm -rf objs/ bin/ __pycache__/ ../__pycache__/

# TODO: Less garbage testing
test:
	$(PY) -m doctest utils.py
	$(PY) -m doctest leaderboard.py