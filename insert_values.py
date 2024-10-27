#!/usr/bin/env python3
import os
file = "Tidal.txt"
def main():
    if not os.path.exists(file):
        with open(file, "w") as f:
            pos = 0
            description = input("quick description of the market: ")
            answer = input("answer to the market: ")
            answer=answer.strip(",")
            description=description.strip(",")
            f.write(f"{pos},{description},{answer}")
    else:
        with open(file, "a") as f:
            pos = 0
            description = input("quick description of the market: ")
            answer = input("answer to the market: ")
            answer=answer.strip(",")
            description=description.strip(",")
            f.write(f"{pos},{description},{answer}")



if __name__ == "__main__":
    _ = main()