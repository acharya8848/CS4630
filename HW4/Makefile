CXX = gcc
CXXFLAGS = -Wall -Werror -pedantic -Og -g -fsanitize=address -fsanitize=undefined -std=c17 -D_GLIBCXX_DEBUG

all: hw4

benign:
	@./gen_benign_input.sh
	./dumbledore.exe < input.txt

crash:
	@./gen_crash_input.sh
	./dumbledore.exe < input.txt

hacked:
	@./gen_hacked_input.sh
	./dumbledore.exe < input.txt

A:
	@./test_all.sh

clean:
	rm -f *.o

.PHONY: clean all benign crash hacked A
