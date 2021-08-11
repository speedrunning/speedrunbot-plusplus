.POSIX:
.SUFFIXES:
CC	= cc

shprogs	= bin/compile

all: bin/ ${shprogs}


#### SHELL ####
bin/compile: compile.sh
	chmod +x $<
	[ -e $@ ] || ln $< $@


#### OTHER ####
bin/:
	mkdir -p bin/


clean:
	rm -rf bin/
.PHONY: clean
