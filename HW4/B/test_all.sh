#!/bin/env bash

CXX=gcc
CXXFLAGS="-Wall -Werror -pedantic -Og -g -fsanitize=address -fsanitize=undefined -std=c17 -D_GLIBCXX_DEBUG"

printf "=%.0s" {1..80}
echo
echo -n "Testing benign input..."
if [ ! -f "./benign" ]; then
	echo -n "generator not found, compiling..."
	$CXX $CXXFLAGS format_string_benign.c -o benign > /dev/null
	if [ $? -ne 0 ]; then
		echo "failed to compile generator!"
		exit 1
	else
		echo -n "done..."
	fi
fi
./benign
OUTPUT="$(./format_string_vulnerability.exe < input.txt)"
if [ $? -ne 0 ]; then
	echo "failed. Program crashed!"
elif echo $OUTPUT | grep -q "I recommend that you get a grade of D on this assignment."; then
	echo "passed."
else
	echo "failed. Program did not print the correct message."
fi
printf "=%.0s" {1..80}
echo
echo -n "Testing attack input..."
if [ ! -f "./attack" ]; then
	echo -n "generator not found, compiling..."
	$CXX $CXXFLAGS format_string_attack.c -o attack > /dev/null
	if [ $? -ne 0 ]; then
		echo "failed to compile generator!"
		exit 1
	else
		echo -n "done..."
	fi
fi
./attack
OUTPUT="$(./format_string_vulnerability.exe < input.txt)"
if [ $? -ne 0 ]; then
	echo "failed. Program crashed!"
elif echo $OUTPUT | grep -q "I recommend that you get a grade of A on this assignment."; then
	echo "passed."
else
	echo "failed. Program did not print the correct message."
fi
printf "=%.0s" {1..80}
echo