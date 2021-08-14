from cs50 import get_int

while True:
    h = get_int('height: ')
    if h < 1 or h > 8:
        h = get_int('height: ')
    if h >= 1 or h <= 8:
        break

for i in range(h):
    print((h - 1 - i) * " ", end="")
    print((i + 1) * "#")