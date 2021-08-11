.POSIX:
.SUFFIXES:
PY	= python3.9

pyprogs	= bin/retime

all: bin/ ${pyprogs}


##### PYTHON #####
bin/retime: retime.py
	cp $< $@
	chmod +x $@


##### OTHER #####
bin/:
	mkdir -p $@

##### PHONY #####
clean:
	rm -rf bin/ __pycache__/ ../__pycache__/
test:
	${PY} -m doctest retime.py
.PHONY: clean test
