.POSIX:
.SUFFIXES:
PY	= python3.9

pyprogs	= bin/recent bin/utils.py

all: bin/ ${pyprogs}


##### PYTHON #####
bin/utils.py: utils.py
	cp $< $@
	chmod +x $@
bin/recent: recent.py
	cp $< $@
	chmod +x $@


##### OTHER #####
bin/:
	mkdir -p $@


##### PHONY ####
clean:
	rm -rf bin/ __pycache__/ ../__pycache__/
.PHONY: clean
