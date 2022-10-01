#!/bin/env bash

# This script generates a benign input that overwrites the padding and touches nothing else.
printf "A%.0s" {1..10} > input.txt
