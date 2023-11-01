# CSP
___
This was my Constraint Satisfication Problem solver for my COSC 76: Artificial Intelligence class. The report on the program implementation is described in the `report.md` file.
___
How to use:

The `ConstraintSatisfactionProblem.py` file contains the implementation for the basic backtracking solver used for the assignment, which is extended by `MapColoringCSP.py` and `CircuitBoardLayoutCSP.py` which uses the CSP solver to solve the specifics related to their problems.

The `MAC3.py` file contains the implementation of the AC3 inference technique, as well as the implementations for the MRV and LCV heuristics. This class is extended by `MapMAC3.py` which utilizes the new implementations on the Map Coloring problem.
