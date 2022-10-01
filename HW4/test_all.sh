#!/bin/env bash

printf "=%.0s" {1..80}
echo
echo -n "Testing benign input..."
./gen_benign_input.sh
if [ $? -ne 0 ]; then
	echo "Failed to generate benign input."
	exit 1
fi
OUTPUT="$(./dumbledore.exe < input.txt)"
if [ $? -ne 0 ]; then
	echo "Dumbledore is dead. What have you done?"
else
	echo "Dumbledore is alive. Good job."
fi
# This is the separator between tests.
printf "=%.0s" {1..80}
echo
echo -n "Testing crash input..."
./gen_crash_input.sh
if [ $? -ne 0 ]; then
	echo "Failed to generate crash input."
	exit 1
fi
OUTPUT="$(./dumbledore.exe < input.txt)"
if [ $? -eq 139 ]; then
	echo "Mission successful. You have killed dumbledore."
elif [ $? -ne 139 && $? -ne 0 ]; then
	echo "Mission successful, but cause of death unknown. Reward cannot be claimed."
else
	echo "Mission failed. We'll get him next time."
fi
# This is the separator between tests.
printf "=%.0s" {1..80}
echo
echo -n "Testing hacked input..."
./gen_hacked_input.sh
if [ $? -ne 0 ]; then
	echo "Failed to generate hacked input."
	exit 1
fi
OUTPUT="$(./dumbledore.exe < input.txt)"
if [ $? -ne 0 ]; then
	echo "Dumbledore is dead. Not the mission?"
# Search for the string "You have been hacked!" in the output using grep.
elif echo "$OUTPUT" | grep -q "You have been hacked!"; then
	echo "Dumbledore has been corrupted. Mission accomplished."
else
	echo "Dumbledore is alive and was not hacked. Pathetic."
fi
printf "=%.0s" {1..80}
echo