CCMP   ?= clang
CFLAGS := -O3 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes \
		-Wno-unused-result
INC    := -I../../include/srcom
PY     := python3.9

cprogs  := bin/categoriesplayed bin/games bin/modcount bin/worldrecords
pyprogs := bin/categories bin/leaderboard bin/runqueue bin/runs bin/verified \
		bin/worldrecord bin/utils.py

all: $(pyprogs) $(cprogs)
$(shell mkdir -p bin/ objs/)

# Python programs

# This needs to retain the file extension for importability
bin/utils.py: utils.py
	chmod +x $< && cp $< $@

bin/%: %.py
	chmod +x $< && cp $< $@

# C programs

# The special rule for `bin/categoriesplayed` and `bin/games` comes first to
# ensure that they don't get linked without `-ljansson`. Additionally, `games`
# and `categoriesplayed` are almost identical, so they both use `games.c`, with
# preproccessor statements.
.PRECIOUS: objs/%.o
objs/categoriesplayed.o: games.c
	$(CCMP) $(CFLAGS) $(INC) -DCATEGORIES -o $@ -c $<

objs/%.o: %.c
	$(CCMP) $(CFLAGS) $(INC) -o $@ -c $<

bin/categoriesplayed: objs/categoriesplayed.o objs/utils.o
	$(CCMP) $(CFLAGS) -o $@ $^ -lcurl -ljansson

bin/games: objs/games.o objs/utils.o
	$(CCMP) $(CFLAGS) -o $@ $^ -lcurl -ljansson

bin/%: objs/%.o objs/utils.o
	$(CCMP) $(CFLAGS) -o $@ $^ -lcurl

# Phony targets
.PHONY: clean test
clean:
	rm -rf objs/ bin/ __pycache__/ ../__pycache__/

test:
	$(PY) -m doctest leaderboard.py
	$(PY) -m doctest runs.py
	$(PY) -m doctest utils.py
	$(PY) -m doctest verified.py