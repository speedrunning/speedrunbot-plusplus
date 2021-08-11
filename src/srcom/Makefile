.POSIX:
.SUFFIXES:
CC	= cc
CFLAGS	= -O3 -pipe -march=native -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes \
	  -I ../../include
CURL	= $$(curl-config --libs) -Wl,-rpath $$(curl-config --prefix)/lib
PY	= python3.9

cprogs	= bin/categories bin/runs
goprogs	= bin/categoriesplayed bin/games bin/modcount bin/runqueue bin/podiums bin/worldrecords
pyprogs	= bin/leaderboard bin/pending bin/verified bin/verifierleaderboard bin/worldrecord bin/whois \
	  bin/utils.py
shprogs	= bin/posts

all: bin/ ${cprogs} ${goprogs} ${pyprogs} ${shprogs}


##### C #####
bin/categories: categories.c utils.c
	${CC} ${CFLAGS} -o $@ $< utils.c ${CURL} -ljansson


##### GOLANG #####
bin/categoriesplayed: games.go.m4 utils.go
	m4 $< >tmp.go
	go build -o $@ tmp.go utils.go
	rm tmp.go
bin/games: games.go.m4 utils.go
	m4 -DGAMES $< >tmp.go
	go build -o $@ tmp.go utils.go
	rm tmp.go
bin/modcount: modcount.go utils.go
	go build -o $@ $< utils.go
bin/runqueue: runqueue.go utils.go
	go build -o $@ $< utils.go
bin/runs: runs.go utils.go
	go build -o $@ $< utils.go
bin/podiums: podiums.go utils.go
	go build -o $@ $< utils.go
bin/worldrecords: worldrecords.go utils.go
	go build -o $@ $< utils.go


##### PYTHON #####
bin/utils.py: utils.py.m4
	m4 $< >$@
	chmod +x $@
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
