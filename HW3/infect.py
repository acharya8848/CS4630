#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Path: HW3\mod.py

TARGET_FILE = 'target.exe'
NEW_TARGET_FILE = 'target.h@kd.exe'
PRINT_FORMAT = b'%s\0'
TEXT_PRINT = b'Wahoo virus infection!\r\n\0'
BASE_ADDR = 0x08048000 # Default entry point for an x86 ELF file

def main():
	data = b''
	# Read the bytes from the target file into a list
	with open(TARGET_FILE, 'rb') as f:
		data = f.read()
	# Check if the file is an ELF file
	if data[0:4] != b'\x7fELF':
		print('Not an ELF file')
		exit(1)
	in_sequence = False
	leave_found = False
	zero_found = False
	code_found = False
	jump_found = False
	string_found = False
	zero_count = 0
	nop_count = 0
	jump_offset = -1
	code_offset = -1
	string_offset = -1
	# Loop through the bytes and find a return opcode with 4 bytes of NOPs
	for i in range(len(data)):
		if in_sequence:
			if data[i] == 0x90:
				nop_count += 1
			elif data[i] == 0x00:
				zero_count += 1
			elif nop_count >= 15 and !code_found:
				code_offset = i - nop_count + 1
				code_found = True
				nop_count = 0
			elif nop_count >= 5 and !jump_found:
				jump_offset = i - nop_count - 1
				jump_found = True
				nop_count = 0
			elif zero_count >= 24 and !string_found:
				string_offset = i - zero_count + 1
				string_found = True
				zero_count = 0
			else:
				in_sequence = False
				nop_count = 0
		else:
			if data[i] == 0xC9: # Find the leave opcode
				leave_found = True
			elif data[i] == 0xC3 and leave_found: # Find the return opcode
				in_sequence = True
				leave_found = False
			elif data[i] == 0x00: # Find the zero opcode
				in_sequence = True
	# Now that a suitable place has been found, save the offset to save the jump opcode
	if jump_offset == -1 or code_offset == -1 or string_offset == -1:
		print('Could not find a suitable place to insert the virus')
		exit(1)
	else:
		print(f"Found offsets.\r\nJump: {hex(jump_offset)}\r\nCode: {hex(code_offset)}\r\nString: {hex(string_offset)}")
	jump_offset += BASE_ADDR
	code_offset += BASE_ADDR
	string_offset += BASE_ADDR
	# Now that the offset has been found, insert the virus
	# # Insert the jump opcode
	data = data[:jump_offset] + b'\xE9' + (code_offset).to_bytes(4, 'little') + data[jump_offset + 5:]
	# Insert TEXT_PRINT in place of the zeros
	data = data[:string_offset] + TEXT_PRINT + data[string_offset + len(TEXT_PRINT):]
	string_offset+= len(TEXT_PRINT)
	# Insert the PRINT_FORMAT next to the TEXT_PRINT
	data = data[:string_offset] + PRINT_FORMAT + data[string_offset + len(PRINT_FORMAT):]
	# The code will push the string offset onto the stack, then the print format, then call printf and return
	code = b'\x06' + (string_offset).to_bytes(4, 'little') + b'\x06' + PRINT_FORMAT + b'\x9A\x70\x72\x69\x6E\x74\x66\xC3\xC9'
	# Insert the code
	data = data[:code_offset] + code + data[code_offset + len(code):]

	# Write the bytes to the target file
	with open(NEW_TARGET_FILE, 'wb') as f:
		f.write(data)

if __name__ == '__main__':
	main()