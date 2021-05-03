CCMP   ?= clang
CFLAGS := -O3 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes -Wno-unused-result
INC    := -I../../include

cprogs := bin/compile

all: $(cprogs)
$(shell mkdir -p bin/ objs/)

# C programs

# Some programs (like `bin/compile`) benefit from knowing which compiler was
# used, so we define it.

.PRECIOUS: objs/%.o
objs/%.o: %.c
	$(CCMP) $(CFLAGS) $(INC) -D$(CCMP) -o $@ -c $<

bin/%: objs/%.o
	$(CCMP) -o $@ $^

# Phony targets
.PHONY: clean
clean:
	rm -rf objs/ bin/
