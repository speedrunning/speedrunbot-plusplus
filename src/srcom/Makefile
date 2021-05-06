CCMP   ?= clang
CFLAGS := -O3 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes -Wno-unused-result
# This might be not very good, look into this!!
CURL   := $(shell curl-config --libs) -Wl,-rpath $(shell curl-config --prefix)/lib
INC    := -I../../include
PY     := python3.9

cprogs  := bin/categories bin/categoriesplayed bin/games bin/modcount bin/runqueue bin/runs \
		bin/worldrecords
pyprogs := bin/categories bin/leaderboard bin/pending bin/verified bin/verifierleaderboard \
		bin/worldrecord bin/utils.py

all: $(pyprogs) $(cprogs)
debug: CFLAGS += -DDEBUG
debug: all
$(shell mkdir -p bin/ objs/ ../../cache/srcom/)

# Python programs

# This needs to retain the file extension for importability
bin/utils.py: utils.py
	chmod +x $< && cp $< $@

bin/%: %.py
	chmod +x $< && ln -b $< $@

# C programs

# The special rules for `bin/categoriesplayed`, `bin/games`, etc. comes first to ensure that they
# don't get linked with incorrect libraries. Additionally, `games` and `categoriesplayed` are almost
# identical, so they both use `games.c`, with preproccessor statements to create two seperate
# binaries.
.PRECIOUS: objs/%.o
objs/categoriesplayed.o: games.c
	$(CCMP) $(CFLAGS) $(INC) -DCATEGORIES -o $@ -c $<

objs/%.o: %.c
	$(CCMP) $(CFLAGS) $(INC) -o $@ -c $<

bin/categories: objs/categories.o objs/utils.o
	$(CCMP) -o $@ $^ $(CURL) -ljansson

bin/categoriesplayed: objs/categoriesplayed.o objs/utils.o
	$(CCMP) -o $@ $^ $(CURL) -ljansson

bin/games: objs/games.o objs/utils.o
	$(CCMP) -o $@ $^ $(CURL) -ljansson

bin/runqueue: objs/runqueue.o objs/utils.o
	$(CCMP) -o $@ $^ $(CURL) -ljansson -pthread

bin/runs: objs/runs.o objs/utils.o
	$(CCMP) -o $@ $^ $(CURL) -ljansson -pthread

bin/%: objs/%.o objs/utils.o
	$(CCMP) -o $@ $^ $(CURL)

# Phony targets
.PHONY: clean test
clean:
	rm -rf objs/ bin/ __pycache__/ ../__pycache__/

test:
	$(PY) -m doctest leaderboard.py
	$(PY) -m doctest utils.py 2>/dev/null
