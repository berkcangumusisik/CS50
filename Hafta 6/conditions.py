from cs50 import get_int

x = get_int("x: ")
y = get_int("y: ")

if x < y:
    print("y, x'ten büyüktür.")
elif x > y:
    print("x, y'den büyüktür.")
else:
    print("x, y'ye eşittir")