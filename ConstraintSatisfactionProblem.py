import copy

class ConstraintSatisfactionProblem:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.assignment = {}


    def is_consistent(self, var, value):
        # The original consistency checks:
        for constraint in self.constraints:
            if var in constraint:
                o_var = constraint[0] if constraint[1] == var else constraint[1]
                if o_var in self.assignment and self.assignment[o_var] == value:
                    return False
        return True

    def select_unassigned_variable(self):
        for var in self.variables:
            if var not in self.assignment:
                return var
        return None

    def order_domain_values(self, var):
        return self.domains[var]


    def backtrack(self):
        if len(self.assignment) == len(self.variables):
            return self.assignment

        var = self.select_unassigned_variable()
        if var is None:
            return None

        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                self.assignment[var] = value
                result = self.backtrack()
                if result:
                    return result
                del self.assignment[var]
        return None
