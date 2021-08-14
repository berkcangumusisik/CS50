import csv
file = open("phonebook.csv", "a")

name = input("İsim giriniz:")
number = int(input("Numara Giriniz:"))

writer = csv.writer(file)
writer.writerow([name, number])
file.close()