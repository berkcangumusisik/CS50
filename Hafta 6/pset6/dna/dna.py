  
from sys import argv, exit
import itertools
import csv
import re
if len(argv) != 3:
    print(f"Error there should be 2 argv, you have {argv}")
    exit(1)

with open(argv[1],"r") as inputfile:
    reader = list(csv.reader(inputfile))
    reader[0].remove("name")
    i = reader[0]

with open(argv[2],"r") as sequence:
    data = sequence.read()

valuelist = []
for q in range(len(i)): 
    maxcounter = 0
    counter = 0
    position = 0
    previouspos = 0
    while position < len(data):
        position = data.find(i[q], position)
        if position == -1: 
            counter = 0
            break

        elif (position != -1) and previouspos == 0:
            counter += 1
            maxcounter = counter
            previouspos = position
        elif (position != -1) and ((position - len(i[q])) == previouspos):
            counter += 1
            previouspos = position
            if maxcounter < counter:
                maxcounter = counter
        elif (position != -1) and ((position - len(i[q])) != previouspos):
            counter = 1
            previouspos = position
            if maxcounter < counter:
                maxcounter = counter
        position += 1
    
    valuelist.append(maxcounter)

valuelist = list(map(str, valuelist))

cleaned = list(reader)
cleaned.pop(0)
for person in cleaned:
    if person[1:] == valuelist:
        print(f"{person[0]}")
        break
    elif person == cleaned[-1]:
        print("No match")