MAN1 := $(shell find . -regex '.*\.1')
MAN5 := $(shell find . -regex '.*\.5')
SU   ?= doas

all:
	$(SU) cp $(MAN1) /usr/share/man/man1/
	$(SU) cp $(MAN5) /usr/share/man/man5/