import sys

filename = input("Enter puzzle filename: ")
grid = []
try:
    with open("instances/" + filename) as file:
        for line in file:
            if line.strip() == "":
                continue
            row = []
            for number in line.split():
                row.append(int(number))
            grid.append(row)
except (FileNotFoundError, ValueError):
    print("Invalid input file.")
    sys.exit()

size = len(grid)

if size == 0:
    print("The puzzle is empty.")
    sys.exit()

for row in grid:
    if len(row) != size:
        print("The grid must be square.")
        sys.exit()

for row in grid:
    print(row)
