from cs50 import get_int


def main():
    while True:
        h = get_int("Height: ")
        width = h
        if h > 0 and h < 9:
            break

    for i in range(1, h + 1):
        num_hashes = i
        num_spaces = width - num_hashes

        print(" " * num_spaces, end="")
        print("#" * num_hashes, end="")

        print("  ", end="")

        print("#" * num_hashes)


if __name__ == "__main__":
    main()