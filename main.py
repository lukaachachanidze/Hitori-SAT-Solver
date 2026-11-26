import sys
import subprocess
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

#for row in grid:
    #print(row)

#print("SAT Variables")
for i in range(size):
    for j in range(size):
        variable = i*size +j +1
        #print(variable, end = " ")
    #print()
clauses = []
#print("duplicate numbers in rows: ")

for i in range(size):
    for j in range(size):
        for k in range(j+1,size):
            if grid[i][j] == grid[i][k]:
                first = i*size + j +1
                second = i*size + k +1
                clauses.append([first,second])


#print("duplicate numbers in colums: ")
for j in range(size):
    for i in range(size):
        for k in range(i+1,size):
            if grid[i][j] == grid[k][j]:
                first=i*size + j +1
                second=k*size + j +1
                clauses.append([first,second])

#print("adjacent black cells: ")
for i in range(size):
    for j in range(size):
        current=i*size +j+1
        if j+1<size:
            right=i*size +j+2
            clauses.append([-current,-right])
        if i+1 <size:
            below= (i+1)*size +j +1
            clauses.append([-current,-below])

roots = []

for i in range(size*size):
    roots.append(size*size+i+1)
clauses.append(roots)

for i in range(size*size):
    clauses.append([-roots[i], -(i+1)])
for i in range(len(roots)):
    for j in range(i+1 , len(roots)):
        clauses.append([-roots[i], -roots[j]])


reach = []
next_variable = 2*size*size + 1

for step in range(size * size):
    layer = []
    for cell in range(size * size):
        layer.append(next_variable)
        next_variable += 1
    reach.append(layer)


for cell in range(size * size):
    clauses.append([-roots[cell], reach[0][cell]])
    clauses.append([-reach[0][cell], roots[cell]])


for step in range(size * size):
    for cell in range(size * size):
        clauses.append([-reach[step][cell], -(cell + 1)])


for step in range(1, size * size):
    for i in range(size):
        for j in range(size):
            cell = i * size + j

            clause = [-reach[step][cell], reach[step - 1][cell]]

            if i > 0:
                clause.append(reach[step - 1][cell - size])

            if i < size - 1:
                clause.append(reach[step - 1][cell + size])

            if j > 0:
                clause.append(reach[step - 1][cell - 1])

            if j < size - 1:
                clause.append(reach[step - 1][cell + 1])

            clauses.append(clause)


for cell in range(size * size):
    clauses.append([cell + 1, reach[size * size - 1][cell]])




print("number of clauses", len(clauses) )
#for clause in clauses:
    #print(clause)
   

with open("output.cnf","w") as file:
    file.write("p cnf " + str(next_variable-1) + " " + str(len(clauses)) + "\n")
    for clause in clauses:
        for number in clause:
            file.write(str(number)+ " ")
        file.write("0\n")
print("cnf file created")



result = subprocess.run(
    ["wsl", "bash", "-c", "$HOME/glucose/simp/glucose -model output.cnf"],   #as i write on windows and i use wsl
    capture_output=True,
    text=True
)





black_cells = []

for line in result.stdout.splitlines():
    if line.startswith("v "):
        for number in line.split()[1:]:
            value = int(number)
            if 1 <= value <= size * size:
                black_cells.append(value)



if "s SATISFIABLE" in result.stdout:
    print("Solution:")
    for i in range(size):
        for j in range(size):
            cell = i * size + j + 1
            if cell in black_cells:
                print("X", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()
elif "s UNSATISFIABLE" in result.stdout:
    print("No solution exists.")
else:
    print("Solver error.")
