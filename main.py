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

print("SAT Variables")
for i in range(size):
    for j in range(size):
        variable = i*size +j +1
        print(variable, end = " ")
    print()
clauses = []
print("duplicate numbers in rows: ")

for i in range(size):
    for j in range(size):
        for k in range(j+1,size):
            if grid[i][j] == grid[i][k]:
                first = i*size + j +1
                second = i*size + k +1
                clauses.append([first,second])


print("duplicate numbers in colums: ")
for j in range(size):
    for i in range(size):
        for k in range(i+1,size):
            if grid[i][j] == grid[k][j]:
                first=i*size + j +1
                second=k*size + j +1
                clauses.append([first,second])

print("adjacent black cells: ")
for i in range(size):
    for j in range(size):
        current=i*size +j+1
        if j+1<size:
            right=i*size +j+2
            clauses.append([-current,-right])
        if i+1 <size:
            below= (i+1)*size +j +1
            clauses.append([-current,-below])


print("number of clauses", len(clauses) )
for clause in clauses:
    print(clause)

with open("output.cnf","w") as file:
    file.write("p cnf " + str(size*size) + " " + str(len(clauses)) + "\n")
    for clause in clauses:
        for number in clause:
            file.write(str(number)+ " ")
        file.write("0\n")
print("cnf file created")