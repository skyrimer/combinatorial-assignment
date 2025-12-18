import gurobipy as gp
from gurobipy import GRB
from data_definitions import get_data
from constraints import calculate_parameters, print_solution


def solve_advanced_case():
    students, courses, capacities, credits, preferences = get_data()
    ranks, top_2, weights = calculate_parameters(
        students, courses, preferences, credits
    )

    # 2. Model Setup
    m = gp.Model("CourseAllocation_AdvancedCase")

    # Variables
    x = {
        (i, j): m.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
        for i in students
        for j in courses
    }
    l = {i: m.addVar(vtype=GRB.BINARY, name=f"l_{i}") for i in students}
    # New Variable: Capacity increase n_j (0, 1, or 2)
    n = {j: m.addVar(vtype=GRB.INTEGER, lb=0, ub=2, name=f"n_{j}") for j in courses}

    # Total Satisfaction Expression
    total_satisfaction = gp.quicksum(
        weights[j] * (6 - ranks[(i, j)]) * x[(i, j)]
        for i in students
        for j in preferences[i]
    )

    # Student 8 Satisfaction Expression
    student_8_satisfaction = gp.quicksum(
        weights[j] * (6 - ranks[(8, j)]) * x[(8, j)] for j in preferences[8]
    )

    # Big M for Hierarchical Optimization (Prioritize Student 8)
    M = 1000
    m.setObjective(M * student_8_satisfaction + total_satisfaction, GRB.MAXIMIZE)

    # Constraints
    # C1: Flexible Capacity (Sum x <= Cap + n)
    for j in courses:
        m.addConstr(
            gp.quicksum(x[(i, j)] for i in students) <= capacities[j] + n[j],
            name=f"Cap_{j}",
        )

    # C1_New: Total Capacity Increase Limit (Sum n <= 2)
    m.addConstr(gp.quicksum(n[j] for j in courses) <= 2, name="Total_Cap_Increase")

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

    # C6_New: Mutual Exclusivity (Algebra & Analytics)
    for i in students:
        m.addConstr(x[(i, "Algebra")] + x[(i, "Analytics")] <= 1, name=f"Conflict_{i}")

    # 3. Solve and Report
    m.optimize()

    # Custom reporting for Advanced Case (to show capacity increases)
    if m.status == GRB.OPTIMAL:
        print_solution(
            m, students, courses, x, weights, ranks, credits, "Advanced Case"
        )

        print("\nCapacity Increases (n_j):")
        for j in courses:
            if n[j].X > 0.5:
                print(f"  {j}: +{int(n[j].X)}")

        # Objective Breakdown
        total_sat_val = sum(
            weights[j] * (6 - ranks[(i, j)]) * x[(i, j)].X
            for i in students
            for j in preferences[i]
            if x[(i, j)].X > 0.5
        )
        s8_sat_val = sum(
            weights[j] * (6 - ranks[(8, j)]) * x[(8, j)].X
            for j in preferences[8]
            if x[(8, j)].X > 0.5
        )

        print(f"\nBreakdown:")
        print(f"  Total Satisfaction Score: {int(total_sat_val)}")
        print(f"  Student 8 Satisfaction:   {int(s8_sat_val)}")


if __name__ == "__main__":
    solve_advanced_case()
