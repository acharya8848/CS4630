#!/usr/bin/env python

def main():
    padding = "Anubhav Acharya. This is the padding that will fill the buffer."
    print(len(padding))
    while len(padding) != 116:
        padding+= "A"

    formatted_padding = ""
    for i in range(0, len(padding)):
        formatted_padding+= ("'" + padding[i] + "', ")

    print(formatted_padding)

if __name__ == "__main__":
    main()
