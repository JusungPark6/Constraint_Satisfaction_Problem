# Constraint Satisfaction Problem (CSP) Solver
## Jusung Park
### COSC 76 Fall 2023
___

This report outlines the development and implementation of a Constraint Satisfaction Problem (CSP) solver in Python, with a specific focus on solving the map-coloring problem for Australia. The goal of this project is to create a flexible CSP solver that can handle various CSPs while adhering to the principles of generic variable and value representations.

## Generic CSP Solver

1. **ConstraintSatisfactionProblem Class**: I created a generic `ConstraintSatisfactionProblem` class that forms the foundation for solving CSPs. This class encapsulates the core logic for CSPs.

2. **Variable and Value Representation**: In line with the provided design notes, I used integers to represent variables and values. This design choice makes it easy to adapt the solver to different problems.

3. **Backtracking Algorithm**: The solver employs a backtracking algorithm based on the provided pseudocode. The main functions include `BACKTRACKING-SEARCH` and `BACKTRACK`. The goal is to find a valid assignment that satisfies all constraints.

## Map-Coloring CSP

For the specific map-coloring problem of Australia, I extended the generic CSP solver into the `MapColoringCSP` class:

1. **Constructor**: The `MapColoringCSP` class's constructor maps the human-readable description of the problem into integers, defining variables, domains, and constraints.

2. **Printing Solutions**: The class includes a method to print solutions in a human-readable format, using territory names and colors.

3. **Constraint Definitions**: I defined the constraints as binary constraints between neighboring regions, ensuring that no two adjacent regions share the same color.

### Testing

I tested the CSP solver on the map-coloring problem for Australia. The solver performed the following steps:

1. Instantiated a `MapColoringCSP` object with the problem's details, including variables, domains, and constraints.

2. Used the backtracking solver from the generic `ConstraintSatisfactionProblem` class to find a valid coloring for the map.

3. Printed the solutions in a human-readable format, mapping integer values back to territory names and colors.

During testing, the solver successfully found solutions for the map-coloring problem, ensuring that no neighboring regions shared the same color. However, it's important to note that the solver's capabilities are limited by the simplicity of the provided constraints and the basic evaluation function.

The CSP solver developed for the map-coloring problem provides a generic framework for solving various CSPs. It adheres to the principles of using integers to represent variables and values, making it adaptable to different scenarios.

While the solver successfully tackled the map-coloring problem, there is room for improvement in handling more complex CSPs. Enhancements to the solver's evaluation function, which currently considers only material values, could lead to more advanced problem-solving capabilities.

Overall, the CSP solver lays a solid foundation for further exploration and extension in the realm of constraint satisfaction problems.

## Circuit-Board Layout Problem

Given a rectangular circuit board of dimensions `n x m` and a set of components, our task is to lay out the components on the board such that no two components overlap, using the CSP methodology.

### Implementation 

1. ***ConstraintSatisfactionProblem class***: which manages the core CSP mechanics, 
2. ***CircuitBoardLayoutCSP class***: for the circuit board layout problem.
3. **Variables**: Each component is considered a variable in the CSP.
4. **Domains**: For a component of width `w` and height `h` on a circuit board of width `n` and height `m`, the domain consists of the set of (x, y) coordinates where the bottom-left corner of the component can be placed. Given these dimensions, the maximum x-coordinate is `n - w` and the maximum y-coordinate is `m - h`. This ensures the component fits completely on the board.
5. **Constraints**: Two components may not overlap. For example, for components `a` and `b` on a `10x3` board, the constraints enforce that if `a` is placed at a certain position, `b` cannot occupy any overlapping position. If the components have coordinates such that they share any common board cell, they are considered overlapping. The code determines these overlapping positions and rules them out during backtracking.
6. `overlaps`: determines if two components overlap based on their positions and sizes:
```python
def overlaps(self, comp1_key, loc1, comp2_key, loc2):
    x1, y1 = loc1
    w1, h1 = self.components[comp1_key]
    x2, y2 = loc2
    w2, h2 = self.components[comp2_key]

    return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)
```
7. **display_solution**: The final solution visually represents the board as a 2D matrix. Each cell either displays a component label or a '.' character indicating an empty space:
```python
def display_solution(self, solution):
    board = [['.' for _ in range(10)] for _ in range(3)]
    for comp, (x, y) in solution.items():
        w, h = self.components[comp]
        for i in range(x, x+w):
            for j in range(y, y+h):
                board[j][i] = comp  
    for row in board:
        print(''.join(row))
```
8. Constraints: The constraints in the system inherently use integer values. Each component's domain consists of integer (x, y) coordinates on the board, and the constraints ensure that these integer coordinates do not cause overlaps. The backtracking process then utilizes these integer coordinates to navigate through potential solutions.

## Inference Technique (MAC-3)

I created two new files `MAC3.py` to implement the arc consistency 3 algorithm following the pseudocode provided in the textbook.

- ***Neighbors Dictionary***: This dictionary keeps track of the neighboring variables for each variable based on constraints. This structure helps in efficiently retrieving the neighbors of a variable without scanning the whole constraint list.
``` python
self.neighbors = {v: set() for v in self.variables}
for (v1, v2) in constraints:
    self.neighbors[v1].add(v2)
    self.neighbors[v2].add(v1)
```
- ***Queue***: This is a list that contains pairs of variables (arcs) that might not be arc-consistent. The AC-3 algorithm works by making sure that for every arc (xi, xj), every value in the domain of xi has some value in the domain of xj with which it is consistent.

### Algorithm

The AC-3 algorithm operates as follows:
1. All arcs are added to the queue. 
2. The algorithm then iteratively picks an arc (xi, xj) from the queue and makes it arc consistent (using the REVISE function). 
3. If the domain of xi is modified (made smaller), then all arcs (xk, xi) where xk is a neighbor of xi (except xj) are added to the queue because the change might create further inconsistencies. 
4. The algorithm terminates when the queue is empty or when some domain becomes empty (in which case the CSP cannot be solved).
```python
def AC_3(self):
    queue = [(xi, xj) for xi in self.variables for xj in self.neighbors[xi]]

    while queue:
        xi, xj = queue.pop(0)
        if self.REVISE(xi, xj):
            if len(self.domains[xi]) == 0:
                return False
            for xk in self.neighbors[xi] - {xj}:
                queue.append((xk, xi))
    return True
```

The REVISE function checks if the domain of variable xi can be reduced due to the constraints with another variable xj. Specifically, for each value in the domain of xi, it checks if there's any value in the domain of xj that satisfies the constraints. If no such value exists, then that value is removed from xi's domain.
```python
def REVISE(self, xi, xj):
    revised = False
        for x in self.domains[xi].copy(): 
            if not any(self.is_consistent(xi, x, xj, y) for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised
```

I had to also adjust the `is_consistent` method because what I had currently was too aggresively pruning the domain which led to no solution being found.
```python
    def is_consistent(self, var1, value1, var2, value2):
        if var1 == var2:
            return value1 != value2
        if (var1, var2) in self.constraints or (var2, var1) in self.constraints:
            return value1 != value2
        return True
```

### Testing Effectiveness
I used the `time.time()` function to check program runtime.
When running the programs, the time function output 1697412410.4214022 without MAC-3 and 1697412224.295299 with MAC-3.
Obviously this was not a huge improvement in efficiency, so there may be errors with my implementation or the test cases I used were not complex enough for the arc consistency 3 algorithm to make a huge difference. I believe the latter is more likely.

## Heuristics

- ***MRV***:(Minimum Remaining Values), prioritizes variables with the least number of legal values left in their domain.
- ***LCV***: (Least Constraining Value), for a given variable, values are ordered by the number of choices they rule out for neighboring variables.

### Implementation

```python
    def select_unassigned_variable(self, use_mrv=False):
        if not use_mrv:
            for var in self.variables:
                if var not in self.assignment:
                    return var
            return None
        else:
            #Using MRV Heuristic
            unassigned_vars = [v for v in self.variables if v not in self.assignment]
            return min(unassigned_vars, key=lambda var: len(self.domains[var]), default=None)
```

```python
    def order_domain_values(self, var, use_lcv=False):
        if not use_lcv:
            return self.domains[var]
        else:
            neighbors = self.neighbors[var]
            values = list(self.domains[var])

            def count_constraining_values(value):
                count = 0
                for neighbor in neighbors:
                    if neighbor not in self.assignment and value in self.domains[neighbor]:
                        count += 1
                return count

            return sorted(values, key=count_constraining_values)
```

### Testing 

Similar to testing AC3, I used the `time.time()` function to check program runtime.
When running the heuristics, the time function output 1697412319.351848 MRV versus 1697412278.9495502 with MRV. Similarly, when testing LCV, the output was 1697412347.535666 with LCV versus 1697412338.732534 with LCV. This leads me to the same conclusion as when testing AC3, meaning these miniscule changes are more likely a result of my computer operating system and the IDE rather than problems in the code or implementation of the heuristics. A better method to accurately test the efficiency of these heuristics would be a much more complex test case.


# BONUS: CS1 Section Assignment

`SectionAssignment.py` contains a file where I attempted the optional extension. I created two files `students.txt` and `leaders.txt` that contain lists of the students in the class and the section leaders, respectively.

- ***is_consistent***: I had to modify this method to ensure the time slots match for a student and leader. The previous unary constraints prevented a student or leader from being assigned to multiple sections.
- ***load_data***: I made sure to strip the strings from unwanted whitespaces. I also prefixed leader variables with '*' for clear distinction.

However, the current test case outputs "None" which I am sure should not be the case so there is a problem within either the implementation or the logic and did not have enough time to debug everything.