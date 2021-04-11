PY     := python3.9

pyprogs := bin/recent bin/utils.py

all: $(pyprogs)
$(shell mkdir -p bin/)

# Python programs

# This needs to retain the file extension for importability
bin/utils.py: utils.py
	chmod +x $< && ln -b $< $@

bin/%: %.py
	chmod +x $< && ln -b $< $@

# Phony targets
.PHONY: clean test
clean:
	rm -rf objs/ bin/ __pycache__/ ../__pycache__/
