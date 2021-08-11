.POSIX:
.SUFFIXES:
shprogs	= bin/compile

all: bin/ ${shprogs}


##### SHELL #####
bin/compile: compile.sh
	cp $< $@
	chmod +x $@


##### OTHER #####
bin/:
	mkdir -p $@


##### PHONY #####
clean:
	rm -rf bin/
.PHONY: clean
