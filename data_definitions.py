def get_data():
    """
    Returns the static data for the course allocation problem.
    """
    # Students 1 to 15

    # Available Courses
    courses = [
        "Algebra",
        "Programming",
        "Statistics",
        "Econometrics",
        "Visualisation",
        "Logic",
        "Analytics",
        "Calculus",
    ]

    # Base Capacities (c_j)
    capacities = {
        "Algebra": 6,
        "Programming": 6,
        "Statistics": 6,
        "Econometrics": 5,
        "Visualisation": 6,
        "Logic": 5,
        "Analytics": 6,
        "Calculus": 5,
    }

    # Credits (k_j)
    credits = {
        "Algebra": 10,
        "Programming": 20,
        "Statistics": 10,
        "Econometrics": 10,
        "Visualisation": 10,
        "Logic": 20,
        "Analytics": 10,
        "Calculus": 20,
    }

    # Student Preferences (Top 5 ordered list)
    preferences = {
        1: ["Analytics", "Statistics", "Programming", "Logic", "Calculus"],
        2: ["Econometrics", "Statistics", "Calculus", "Analytics", "Logic"],
        3: ["Econometrics", "Analytics", "Logic", "Algebra", "Programming"],
        4: ["Analytics", "Statistics", "Visualisation", "Econometrics", "Algebra"],
        5: ["Analytics", "Statistics", "Algebra", "Econometrics", "Visualisation"],
        6: ["Statistics", "Econometrics", "Visualisation", "Logic", "Algebra"],
        7: ["Econometrics", "Analytics", "Visualisation", "Programming", "Algebra"],
        8: ["Econometrics", "Analytics", "Statistics", "Visualisation", "Programming"],
        9: ["Analytics", "Statistics", "Econometrics", "Visualisation", "Programming"],
        10: ["Analytics", "Econometrics", "Algebra", "Programming", "Visualisation"],
        11: ["Econometrics", "Statistics", "Algebra", "Visualisation", "Analytics"],
        12: ["Econometrics", "Analytics", "Algebra", "Visualisation", "Statistics"],
        13: ["Analytics", "Econometrics", "Visualisation", "Algebra", "Statistics"],
        14: ["Econometrics", "Analytics", "Statistics", "Programming", "Visualisation"],
        15: ["Statistics", "Analytics", "Programming", "Calculus", "Visualisation"],
    }
    students = list(sorted(preferences.keys()))
    validate_data(students, courses, capacities, credits, preferences)

    return students, courses, capacities, credits, preferences


def validate_data(students, courses, capacities, credits, preferences):
    assert sorted(courses) == sorted(
        credits.keys()
    ), "Course names and credits do not match"
    assert sorted(courses) == sorted(
        capacities.keys()
    ), "Course names and capacities do not match"

    assert len(students) == len(
        preferences
    ), "Number of students and preferences must match"

    # Validate preferences cover every student and reference valid courses
    assert set(preferences.keys()) == set(
        students
    ), "Preference entries must exist for every student"
    for prefs in preferences.values():
        assert len(prefs) == 5, "Each student should list exactly five preferences"
        assert len(set(prefs)) == 5, "Preferences must consist of unique courses"
        assert all(
            course in courses for course in prefs
        ), "Preferences may only include defined courses"

    assert all(
        isinstance(capacity, int) and capacity >= 0 for capacity in capacities.values()
    ), "Course capacities must be non-negative integers"
    assert all(
        isinstance(credit, int) and credit >= 0 for credit in credits.values()
    ), "Course credits must be non-negative integers"
