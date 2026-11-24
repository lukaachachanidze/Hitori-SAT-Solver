grid = []

with open("instances/example.in") as file:
    for line in file:
        row = []
        for number in line.split():
            row.append(int(number))
        grid.append(row)

for row in grid:
    print(row)