#include <stdio.h>

int main(int argc, char *argv[]) {
	char *buf = "Anubhav Acharya\nAnubhav Acharya";
	FILE *fp = fopen("input.txt", "wb");
	fprintf(fp, "%s", buf);
	fclose(fp);
	return 0;
}