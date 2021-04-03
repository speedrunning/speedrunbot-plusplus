PY     := python3.9

pyprogs := bin/retime

all: $(pyprogs)
$(shell mkdir -p bin/)

# Python programs

# This needs to retain the file extension for importability
bin/%: %.py
	chmod +x $< && cp $< $@

# Phony targets
.PHONY: clean test
clean:
	rm -rf bin/ __pycache__/ ../__pycache__/

test:
	$(PY) -m doctest retime.py
