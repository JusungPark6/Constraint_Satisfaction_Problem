from MAC3 import MAC3


class SectionAssignment(MAC3):
    def __init__(self, student_file, leader_file):
        variables, domains = self.load_data(student_file, leader_file)
        constraints = self.generate_constraints(variables)
        super().__init__(variables, domains, constraints)

    def load_data(self, student_file, leader_file):
        with open(student_file, 'r') as f:
            students = {line.split(",")[0].strip(): set(line.strip().split(",")[1:]) for line in f.readlines()}
        with open(leader_file, 'r') as f:
            leaders = {'*' + line.split(",")[0].strip(): set(line.strip().split(",")[1:]) for line in f.readlines()}

        variables = list(students.keys()) + list(leaders.keys())
        domains = {**students, **leaders}

        return variables, domains

    def generate_constraints(self, variables):
        return [(var1, var2) for i, var1 in enumerate(variables) for j, var2 in enumerate(variables) if i != j]

    def is_consistent(self, var1, value1, var2, value2):
        # Ensure that students aren't assigned to times without leaders
        if '*' in var1 and '*' not in var2:
            return value1 == value2
        elif '*' not in var1 and '*' in var2:
            return value1 == value2
        # For other cases, check the unary constraints
        elif var1 == var2:
            return value1 != value2
        return True

    # Utility methods for the new constraints
    def create_sections(self):
        sections = {}
        for var, time in self.assignment.items():
            if time not in sections:
                sections[time] = []
            sections[time].append(var)
        return sections

    def valid_section_sizes(self, n, k):
        sections = self.create_sections()
        for section, members in sections.items():
            if len(members) < (n / k) - 1 or len(members) > (n / k) + 1:
                return False
        return True

    def section_has_leader(self):
        sections = self.create_sections()
        for section, members in sections.items():
            if not any('*' in member for member in members):
                return False
        return True

    def backtrack(self, use_ac3=False, use_mrv=False, use_lcv=False):
        n = len([var for var in self.variables if '*' not in var])
        k = len([var for var in self.variables if '*' in var])

        # Check our added constraints first to terminate early if they aren't satisfied
        if not self.section_has_leader() or not self.valid_section_sizes(n, k):
            return None
        return super().backtrack(use_ac3, use_mrv, use_lcv)

if __name__ == "__main__":
    solver = SectionAssignment('students.txt', 'leaders.txt')
    solution = solver.backtrack()
    print(solution)
