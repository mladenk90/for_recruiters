# TODO

from cs50 import get_int

while True:
    height = get_int("height: ")
    if height > 0 and height < 9:
        break

for i in range(0, height, 1):
    for j in range(0, height, 1):
        if (i+j < height-1):
            print(" ", end="")
        else:
            print("#", end="")
    print()