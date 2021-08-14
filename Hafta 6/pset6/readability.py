from cs50 import get_string

text = get_string("Text: ")

n_words = n_sent = n_let = i = 0
length = len(text)

while i < length:
    if text[i].isalpha():
        n_let += 1
    if (i == 0 and text[i] != " ") or (i != length and text[i] == " " and text[i + 1] != " "):
        n_words += 1
    if text[i] == "." or text[i] == "?" or text[i] == "!":
        n_sent += 1
    i += 1

L = (n_let / n_words) * 100
S = (n_sent / n_words) * 100
index = round(0.0588 * L - 0.296 * S - 15.8)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")