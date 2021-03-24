CCMP   ?= clang
CFLAGS := -O3 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes \
		-Wno-unused-result
INC    := -I../../include

cprogs := bin/compile

all: $(cprogs)
$(shell mkdir -p bin/ objs/)

# C programs

.PRECIOUS: objs/%.o
objs/%.o: %.c
	$(CCMP) $(CFLAGS) $(INC) -o $@ -c $<

bin/%: objs/%.o
	$(CCMP) $(CFLAGS) -o $@ $^

# Phony targets
.PHONY: clean
clean:
	rm -rf objs/ bin/