from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
import time
class MapColoringCSP(ConstraintSatisfactionProblem):
    def __init__(self, variables, colors, constraints):
        self.variables = variables
        self.domains = {var: colors for var in self.variables}
        self.constraints = constraints
        super().__init__(self.variables, self.domains, self.constraints)

    def print_solution(self, assignment):
        for var, value in assignment.items():
            print(f"{var} = {value}")


# Instantiate and solve the map-coloring problem
if __name__ == "__main__":
    variables = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
    colors = ["red", "green", "blue"]
    constraints = [
            ("SA", "WA"), ("SA", "NT"), ("SA", "Q"), ("SA", "NSW"), ("SA", "V"),
            ("WA", "NT"), ("NT", "Q"), ("Q", "NSW"), ("NSW", "V")
        ]
    map_coloring_problem = MapColoringCSP(variables, colors, constraints)
    solution = map_coloring_problem.backtrack()
    map_coloring_problem.print_solution(solution)
    print(time.time())
