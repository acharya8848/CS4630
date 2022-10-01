#!/bin/env bash

# This script generates an input that will crash the program.
printf "A%.0s" {1..40} > input.txt
