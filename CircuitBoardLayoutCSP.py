from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
import time
class CircuitBoardLayoutCSP(ConstraintSatisfactionProblem):
    def __init__(self, board_width, board_height, components):
        self.components = components
        variables = list(components.keys())
        self.board_width = board_width
        self.board_height = board_height
        domains = self.compute_domains(board_width, board_height)
        constraints = self.compute_constraints(variables)
        super().__init__(variables, domains, constraints)

    def compute_domains(self, board_width, board_height):
        domains = {}
        for key, (w, h) in self.components.items():
            domains[key] = [(x, y) for x in range(board_width - w + 1) for y in range(board_height - h + 1)]
        return domains

    def compute_constraints(self, variables):
        constraints = []
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                constraints.append((variables[i], variables[j]))
        return constraints

    def overlaps(self, comp1_key, loc1, comp2_key, loc2):
        x1, y1 = loc1
        w1, h1 = self.components[comp1_key]
        x2, y2 = loc2
        w2, h2 = self.components[comp2_key]

        if x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1:
            return False
        return True

    def is_consistent(self, var, value):
        for other_var, other_value in self.assignment.items():
            if self.overlaps(var, value, other_var, other_value):
                return False
        return True
    def display_solution(self, solution):
        # Initialize the board with '.'
        board = [['.' for _ in range(self.board_width)] for _ in range(self.board_height)]

        for comp, (x, y) in solution.items():
            w, h = self.components[comp]
            for i in range(x, x + w):
                for j in range(y, y + h):
                    board[j][i] = comp  # Place the component on the board

        # Print the board
        for row in board:
            print(''.join(row))

# Example usage:
components = {
    'a': (3, 2),
    'b': (5, 2),
    'c': (2, 3),
    'e': (7, 1)
}

csp = CircuitBoardLayoutCSP(10, 3, components)

solution = csp.backtrack()
print(solution.items())
csp.display_solution(solution)
print(time.time())
