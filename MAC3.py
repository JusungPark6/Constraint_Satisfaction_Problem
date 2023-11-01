import copy

class MAC3:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.assignment = {}
        self.neighbors = {v: set() for v in self.variables}
        for (v1, v2) in constraints:
            self.neighbors[v1].add(v2)
            self.neighbors[v2].add(v1)  # constraints are bi-directional

    def is_consistent(self, var1, value1, var2, value2):
        if var1 == var2:
            return value1 != value2
        if (var1, var2) in self.constraints or (var2, var1) in self.constraints:
            return value1 != value2
        return True
        # for constraint in self.constraints:
        #     if var in constraint:
        #         o_var = constraint[0] if constraint[1] == var else constraint[1]
        #         if o_var in self.assignment and self.assignment[o_var] == value:
        #             return False
        # return True

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

    def REVISE(self, xi, xj):
        revised = False
        for x in self.domains[xi].copy():  # Make a copy so we can modify in-place
            # Check if there's any value in xj's domain that's consistent with x of xi.
            if not any(self.is_consistent(xi, x, xj, y) for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def backtrack(self, use_ac3=False, use_mrv=False, use_lcv=False):
        # If AC-3 is enabled, run it to prune domains
        if use_ac3 and not self.AC_3():
            return None  # return None if AC-3 detects no solution possible

        # If all variables are assigned, return the assignment as the solution
        if len(self.assignment) == len(self.variables):
            return self.assignment

        # Select the next variable to assign based on the MRV heuristic or not
        var = self.select_unassigned_variable(use_mrv=use_mrv)
        if var is None:
            return None  # No variables left to assign, return None

        # Iterate through the domain of the variable (potentially ordered by LCV)
        for value in self.order_domain_values(var, use_lcv=use_lcv):
            if all(self.is_consistent(var, value, assigned_var, assigned_value) for assigned_var, assigned_value in
                   self.assignment.items()):
                # Assign the value and proceed with backtracking
                self.assignment[var] = value
                result = self.backtrack(use_ac3=use_ac3, use_mrv=use_mrv, use_lcv=use_lcv)
                # If result is not None, a solution was found, so return it
                if result:
                    return result

                # Remove the assignment (backtrack)
                del self.assignment[var]

        return None  # No valid assignment was found for this variable at this level