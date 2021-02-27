CC     := cc
CFLAGS := -O3 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes -Wno-unused-result
INC    := -I../../include/srcom
PY     := python3.9

cprogs  := bin/games bin/modcount bin/wrs
pyprogs := bin/categories bin/leaderboard bin/runs bin/verified bin/worldrecord \
			bin/utils.py

all: $(pyprogs) $(cprogs)
$(shell mkdir -p bin/ objs/)

# Python programs

# This needs to retain the file extension for importability
bin/utils.py: utils.py
	chmod +x $< && cp $< $@

bin/%: %.py
	chmod +x $< && cp $< $@

# C programs

# The special rule for `bin/games` comes first to ensure that it doesn't get
# linked without `-ljansson`
.PRECIOUS: objs/%.o
objs/%.o: %.c
	$(CC) $(CFLAGS) $(INC) -o $@ -c $<

bin/games: objs/games.o objs/utils.o
	$(CC) $(CFLAGS) -o $@ $^ -lcurl -ljansson

bin/%: objs/%.o objs/utils.o
	$(CC) $(CFLAGS) -o $@ $^ -lcurl

# Phony targets
.PHONY: clean test
clean:
	rm -rf objs/ bin/ __pycache__/ ../__pycache__/

# TODO: Less garbage testing
test:
	$(PY) -m doctest utils.py
	$(PY) -m doctest leaderboard.py
	$(PY) -m doctest verified.py