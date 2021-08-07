.POSIX:
.SUFFIXES:
CC	= cc
CFLAGS	= -O3 -pipe -march=native -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes \
	  -I ../../include
CURL	= $$(curl-config --libs) -Wl,-rpath $$(curl-config --prefix)/lib
PY	= python3.9

cprogs	= bin/categories bin/runs bin/worldrecords
goprogs	= bin/games bin/modcount bin/runqueue bin/podiums
pyprogs	= bin/leaderboard bin/pending bin/verified bin/verifierleaderboard bin/worldrecord bin/whois \
	  bin/utils.py
shprogs	= bin/posts

all: bin/ ${cprogs} ${goprogs} ${pyprogs} ${shprogs}


##### C #####
bin/categories: categories.c utils.c
	${CC} ${CFLAGS} -o $@ $< utils.c ${CURL} -ljansson
bin/runs: runs.c utils.c
	${CC} ${CFLAGS} -o $@ $< utils.c ${CURL} -ljansson -pthread
bin/worldrecords: worldrecords.c utils.c
	${CC} ${CFLAGS} -o $@ $< utils.c ${CURL}


##### GOLANG #####
bin/games: games.go utils.go
	go build -o $@ $< utils.go
bin/modcount: modcount.go utils.go
	go build -o $@ $< utils.go
bin/runqueue: runqueue.go utils.go
	go build -o $@ $< utils.go
bin/podiums: podiums.go utils.go
	go build -o $@ $< utils.go


##### PYTHON #####
bin/utils.py: utils.py
	chmod +x $<
	cp $< $@
bin/leaderboard: leaderboard.py
	chmod +x $<
	[ -e $@ ] || ln $< $@
bin/pending: pending.py
	chmod +x $<
	[ -e $@ ] || ln $< $@
bin/verified: verified.py
	chmod +x $<
	[ -e $@ ] || ln $< $@
bin/verifierleaderboard: verifierleaderboard.py
	chmod +x $<
	[ -e $@ ] || ln $< $@
bin/worldrecord: worldrecord.py
	chmod +x $<
	[ -e $@ ] || ln $< $@
bin/whois: whois.py
	chmod +x $<
	[ -e $@ ] || ln $< $@

##### SHELL #####
bin/posts: posts.sh
	chmod +x $<
	[ -e $@ ] || ln $< $@


##### OTHER #####
bin/:
	mkdir -p bin/


##### PHONY #####
clean:
	rm -rf bin/ __pycache__/ ../__pycache__/
test:
	${PY} -m doctest leaderboard.py utils.py
.PHONY: clean test
