import gurobipy as gp
from gurobipy import GRB
from data_definitions import get_data
from constraints import calculate_parameters, print_solution


def solve_base_case():
    students, courses, capacities, credits, preferences = get_data()
    ranks, top_2, weights = calculate_parameters(
        students, courses, preferences, credits
    )

    # 2. Model Setup
    m = gp.Model("CourseAllocation_BaseCase")

    # Variables
    # x_{i,j}: whether student i is assigned to class j
    # l_i: binary variable indicating if student i gets a top-2 course
    x = {
        (i, j): m.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
        for i in students
        for j in courses
    }
    l = {i: m.addVar(vtype=GRB.BINARY, name=f"l_{i}") for i in students}

    # Objective: Maximize Satisfaction
    # Sum over all valid assignments: weight * (6 - rank) * x_ij
    m.setObjective(
        gp.quicksum(
            weights[j] * (6 - ranks[(i, j)]) * x[(i, j)]
            for i in students
            for j in preferences[i]
        ),
        GRB.MAXIMIZE,
    )

    # Constraints
    # C1: Course Capacity
    for j in courses:
        m.addConstr(
            gp.quicksum(x[(i, j)] for i in students) <= capacities[j], name=f"Cap_{j}"
        )

    # C2: Credit Limit (<= 40)
    for i in students:
        m.addConstr(
            gp.quicksum(credits[j] * x[(i, j)] for j in courses) <= 40,
            name=f"Credit_{i}",
        )

    # C3: Valid Preferences Only
    for i in students:
        for j in courses:
            if j not in preferences[i]:
                m.addConstr(x[(i, j)] == 0)

    # C4: Global Top-2 Requirement (At least 13 students)
    m.addConstr(gp.quicksum(l[i] for i in students) >= 13, name="Global_Top2")

    # C5: Link Top-2 Variable
    for i in students:
        m.addConstr(
            gp.quicksum(x[(i, j)] for j in top_2[i]) >= l[i], name=f"Link_Top2_{i}"
        )

    # 3. Solve and Report
    m.optimize()
    print_solution(m, students, courses, x, weights, ranks, credits, "Base Case")


if __name__ == "__main__":
    solve_base_case()
