CXX = gcc
CXXFLAGS = -Wall -Werror -pedantic -Og -g -std=c17 -D_GLIBCXX_DEBUG

all: B

benign: format_string_benign.c
	@$(CXX) $(CXXFLAGS) -o $@ $^
	@./benign
	@./format_string_vulnerability.exe < input.txt

attack: format_string_attack.c
	@$(CXX) $(CXXFLAGS) -o $@ $^
	@./attack
	@./format_string_vulnerability.exe < input.txt

B:
	@./test_all.sh

clean:
	rm -f *.o attack benign

.PHONY: clean all benign attack B
