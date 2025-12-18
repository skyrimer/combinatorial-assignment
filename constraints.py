import gurobipy as gp


def calculate_parameters(students, courses, preferences, credits):
    """
    Calculates derived parameters needed for the optimization model.
    """
    # Ranks r_ij: The position (1-5) of course j in student i's list
    ranks = {}
    for i in students:
        for j in preferences[i]:
            ranks[(i, j)] = preferences[i].index(j) + 1

    # Top-2 Sets T2_i: The set of the first two courses for each student
    top_2 = {i: set(preferences[i][:2]) for i in students}

    # Credit Weights z_j: Credit / 10
    weights = {j: credits[j] / 10 for j in courses}

    return ranks, top_2, weights


def print_solution(
    m, students, courses, x, weights, ranks, credits_dict, scenario_name="Solution"
):
    """
    Helper function to print the solution in a standardized format.
    """

    if m.status == gp.GRB.OPTIMAL:
        print(f"\n--- {scenario_name} ---")
        print(f"Optimal Objective Value: {m.objVal}")

        print("\nStudent Assignments:")
        for i in students:
            assigned = [j for j in courses if x[(i, j)].X > 0.5]
            satisfaction = sum(
                weights[j] * (6 - ranks[(i, j)]) for j in assigned if (i, j) in ranks
            )
            total_credits = sum(credits_dict[j] for j in assigned)
            print(
                f"  Student {i:2}: {assigned} (Sat: {int(satisfaction)}, Credits: {total_credits})"
            )
    else:
        print(f"Model did not reach optimality: {m.status}")
