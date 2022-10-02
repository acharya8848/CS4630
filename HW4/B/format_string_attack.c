#include <stdio.h>

int main(int argc, char *argv[]) {
	char *buf = "\x2a\xa0\x04\x08                                                             %23$n\nAnubhav Acharya";
	FILE *fp = fopen("input.txt", "wb");
	fprintf(fp, "%s", buf);
	fclose(fp);
	return 0;
}