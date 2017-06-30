# Makefile for realhud

CFLAGS = -g
LDFLAGS = -L/usr/X11R6/lib -lXpm -lXext -lX11 -lm

all: realhud

realhud: realhud.o
	$(CC) -o realhud realhud.o $(LDFLAGS)

clean:
	-rm -f *.[oas] *.ld core realhud
