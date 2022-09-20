CXX = gcc
CXXFLAGS = -Wall -Werror -pedantic -Og -g -fsanitize=address -fsanitize=undefined -std=c17 -D_GLIBCXX_DEBUG

all: patch

infect: infect.c
	$(CXX) $(CXXFLAGS) -o $@ $^

patch: infect
	./infect
	objdump -d infected-target.exe > target.inf.dmp

clean:
	rm -f *.o infected-target.exe infect

.PHONY: clean all infect
