people = {
    "Brian": "1234567",
    "David": "1234568"
}

name = input("İsim giriniz:")
if name in people:
    print(f"Number: {people[name]}")