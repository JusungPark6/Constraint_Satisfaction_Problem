from MAC3 import MAC3
import time
class MapMAC3(MAC3):
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
    colors = ["red", "green", "blue", "violet", "yellow"]
    constraints = [
            ("SA", "WA"), ("SA", "NT"), ("SA", "Q"), ("SA", "NSW"), ("SA", "V"),
            ("WA", "NT"), ("NT", "Q"), ("Q", "NSW"), ("NSW", "V")
        ]
    map_coloring_problem = MapMAC3(variables, colors, constraints)
    solution = map_coloring_problem.backtrack(use_ac3=True, use_mrv=True, use_lcv=False)
    map_coloring_problem.print_solution(solution)
    print(time.time())
