.POSIX:
.SUFFIXES:
CC	= cc
CFLAGS	= -O3 -pipe -march=native -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes \
	  -I ../../include
CURL	= $$(curl-config --libs) -Wl,-rpath $$(curl-config --prefix)/lib
PY	= python3.9

cprogs	= bin/categories bin/categoriesplayed bin/games bin/runs bin/worldrecords
goprogs	= bin/modcount bin/runqueue bin/podiums
pyprogs	= bin/leaderboard bin/pending bin/verified bin/verifierleaderboard bin/worldrecord \
	  bin/utils.py
shprogs	= bin/posts

all: start ${cprogs} ${goprogs} ${pyprogs} ${shprogs}


##### C #####
bin/categories: categories.c utils.c
	${CC} ${CFLAGS} -o $@ $< utils.c ${CURL} -ljansson
bin/categoriesplayed: games.c utils.c
	${CC} ${CFLAGS} -DCATEGORIES -o $@ $< utils.c ${CURL} -ljansson
bin/games: games.c utils.c
	${CC} ${CFLAGS} -o $@ $< utils.c ${CURL} -ljansson
bin/runs: runs.c utils.c
	${CC} ${CFLAGS} -o $@ $< utils.c ${CURL} -ljansson -pthread
bin/worldrecords: worldrecords.c utils.c
	${CC} ${CFLAGS} -o $@ $< utils.c ${CURL}


##### GOLANG #####
bin/modcount: modcount.go
	go build -o $@ $< utils.go
bin/runqueue: runqueue.go
	go build -o $@ $< utils.go
bin/podiums: podiums.go
	go build -o $@ $< utils.go


##### PYTHON #####
bin/utils.py: utils.py
	chmod +x $< && cp $< $@
bin/leaderboard: leaderboard.py
	chmod +x $< && ln $< $@
bin/pending: pending.py
	chmod +x $< && ln $< $@
bin/verified: verified.py
	chmod +x $< && ln $< $@
bin/verifierleaderboard: verifierleaderboard.py
	chmod +x $< && ln $< $@
bin/worldrecord: worldrecord.py
	chmod +x $< && ln $< $@


##### SHELL #####
bin/posts: posts.sh
	chmod +x $< && ln $< $@


##### PHONY #####
clean:
	rm -rf bin/ __pycache__/ ../__pycache__/
start:
	mkdir -p bin/
.PHONY: clean start
