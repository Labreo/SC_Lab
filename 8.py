def read_value(message):
    while True:
        try:
            value = float(eval(input(message), {"__builtins__": {}}, {}))
            if 0 <= value <= 1:
                return value
            print("Membership value must be between 0 and 1.")
        except:
            print("Enter a valid value like 1/2, 3/4 or 0.75.")


def input_sets():
    print("\nEnter Fuzzy Set Details")

    n = int(input("Enter number of elements in the universe: "))

    universe = []
    A = []
    B = []

    print("\nEnter universe elements:")
    for i in range(n):
        element = input("Element " + str(i + 1) + ": ")
        universe.append(element)

    print("\nEnter membership values for Set A:")
    for i in range(n):
        value = read_value("A(" + universe[i] + ") = ")
        A.append(value)

    print("\nEnter membership values for Set B:")
    for i in range(n):
        value = read_value("B(" + universe[i] + ") = ")
        B.append(value)

    return universe, A, B


def display_set(name, universe, values):
    print("\n" + name)
    print("-" * 35)

    for i in range(len(universe)):
        print(f"{universe[i]} : {values[i]:.3f}")

    formatted = "{" + ", ".join(f"{v:.3f}/{u}" for u, v in zip(universe, values)) + "}"
    print("Fuzzy Set Notation:", formatted)


def display_matrix(name, matrix, row_labels=None, col_labels=None):
    print("\n" + name)
    print("-" * 45)

    if col_labels:
        header = "       " + "  ".join(f"{str(c):>7}" for c in col_labels)
        print(header)

    for i, row in enumerate(matrix):
        row_str = "  ".join(f"{value:7.3f}" for value in row)
        if row_labels:
            print(f"{str(row_labels[i]):>5} : {row_str}")
        else:
            print(f"  {row_str}")


def union(A, B):
    return [max(a, b) for a, b in zip(A, B)]


def intersection(A, B):
    return [min(a, b) for a, b in zip(A, B)]


def complement(A):
    return [round(1 - a, 4) for a in A]


def difference(A, B):
    return [round(min(a, 1 - b), 4) for a, b in zip(A, B)]


def algebraic_sum(A, B):
    return [round(a + b - a * b, 4) for a, b in zip(A, B)]


def algebraic_product(A, B):
    return [round(a * b, 4) for a, b in zip(A, B)]


def bounded_sum(A, B):
    return [min(1.0, round(a + b, 4)) for a, b in zip(A, B)]


def bounded_difference(A, B):
    return [max(0.0, round(a - b, 4)) for a, b in zip(A, B)]


def cartesian_product(A, B, method="min"):
    result = []
    for a in A:
        row = []
        for b in B:
            if method == "min":
                row.append(min(a, b))
            else:
                row.append(round(a * b, 4))
        result.append(row)
    return result


def display_cartesian_product(universe, A, B):
    print("\n========== CARTESIAN PRODUCT OF FUZZY SETS ==========")
    min_prod = cartesian_product(A, B, "min")
    alg_prod = cartesian_product(A, B, "prod")

    display_matrix("Cartesian Product using Min (A x B)", min_prod, universe, universe)
    display_matrix("Cartesian Product using Algebraic Product (A . B)", alg_prod, universe, universe)


def all_operations(universe, A, B):
    print("\n========== ALL FUZZY SET OPERATIONS ==========")

    display_set("Set A", universe, A)
    display_set("Set B", universe, B)

    display_set("Union (A U B)", universe, union(A, B))
    display_set("Intersection (A n B)", universe, intersection(A, B))
    display_set("Complement of A", universe, complement(A))
    display_set("Complement of B", universe, complement(B))
    display_set("Difference (A - B)", universe, difference(A, B))
    display_set("Difference (B - A)", universe, difference(B, A))
    display_set("Algebraic Sum", universe, algebraic_sum(A, B))
    display_set("Algebraic Product", universe, algebraic_product(A, B))
    display_set("Bounded Sum", universe, bounded_sum(A, B))
    display_set("Bounded Difference (A - B)", universe, bounded_difference(A, B))
    display_set("Bounded Difference (B - A)", universe, bounded_difference(B, A))

    display_cartesian_product(universe, A, B)

    print("\n========== DE MORGAN'S LAWS ==========")

    left1 = complement(union(A, B))
    right1 = intersection(complement(A), complement(B))

    left2 = complement(intersection(A, B))
    right2 = union(complement(A), complement(B))

    display_set("Complement of Union [!(A U B)]", universe, left1)
    display_set("Intersection of Complements [!A n !B]", universe, right1)
    law1_holds = all(abs(l - r) < 1e-4 for l, r in zip(left1, right1))
    print("First De Morgan's Law Verified:", law1_holds)

    display_set("Complement of Intersection [!(A n B)]", universe, left2)
    display_set("Union of Complements [!A U !B]", universe, right2)
    law2_holds = all(abs(l - r) < 1e-4 for l, r in zip(left2, right2))
    print("Second De Morgan's Law Verified:", law2_holds)


def input_relation(name):
    print("\nEnter details for Relation", name)

    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))

    matrix = []

    for i in range(rows):
        row = []
        print(f"Enter values for row {i + 1} ({cols} values):")

        for j in range(cols):
            value = read_value(f"Enter {name}[{i + 1}][{j + 1}]: ")
            row.append(value)

        matrix.append(row)

    return matrix


def compose(R, S, method):
    rows = len(R)
    cols = len(S[0])
    common = len(S)

    result = []

    for i in range(rows):
        row = []

        for j in range(cols):
            maximum = 0.0

            for k in range(common):
                if method == "min":
                    value = min(R[i][k], S[k][j])
                else:
                    value = R[i][k] * S[k][j]

                maximum = max(maximum, value)

            row.append(round(maximum, 4))

        result.append(row)

    return result


def max_min_composition():
    print("\n========== MAX-MIN COMPOSITION (R o S) ==========")

    R = input_relation("R")
    S = input_relation("S")

    if len(R[0]) != len(S):
        print("\nComposition is not possible.")
        print(f"Columns of R ({len(R[0])}) must equal rows of S ({len(S)}).")
        return

    result = compose(R, S, "min")

    display_matrix("Relation R", R)
    display_matrix("Relation S", S)
    display_matrix("Max-Min Composition (R o S)", result)


def max_product_composition():
    print("\n========== MAX-PRODUCT COMPOSITION (R . S) ==========")

    R = input_relation("R")
    S = input_relation("S")

    if len(R[0]) != len(S):
        print("\nComposition is not possible.")
        print(f"Columns of R ({len(R[0])}) must equal rows of S ({len(S)}).")
        return

    result = compose(R, S, "prod")

    display_matrix("Relation R", R)
    display_matrix("Relation S", S)
    display_matrix("Max-Product Composition (R . S)", result)


def both_compositions():
    print("\n========== BOTH COMPOSITIONS (MAX-MIN & MAX-PRODUCT) ==========")

    R = input_relation("R")
    S = input_relation("S")

    if len(R[0]) != len(S):
        print("\nComposition is not possible.")
        print(f"Columns of R ({len(R[0])}) must equal rows of S ({len(S)}).")
        return

    display_matrix("Relation R", R)
    display_matrix("Relation S", S)
    display_matrix("Max-Min Composition (R o S)", compose(R, S, "min"))
    display_matrix("Max-Product Composition (R . S)", compose(R, S, "prod"))


def main():
    print("========== FUZZY SET OPERATIONS & COMPOSITIONS ==========")

    universe, A, B = input_sets()

    while True:
        print("\n============== MAIN MENU ==============")
        print("1. Display Sets A and B")
        print("2. Union (Maximum)")
        print("3. Intersection (Minimum)")
        print("4. Complement of A and B")
        print("5. Difference (A - B)")
        print("6. Difference (B - A)")
        print("7. Algebraic Sum")
        print("8. Algebraic Product")
        print("9. Bounded Sum")
        print("10. Bounded Difference")
        print("11. Cartesian Product (Min & Product)")
        print("12. All Set Operations & De Morgan's Laws")
        print("13. Max-Min Composition of Relations")
        print("14. Max-Product Composition of Relations")
        print("15. Both Compositions (Max-Min & Max-Product)")
        print("16. Enter New Sets")
        print("17. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            display_set("Set A", universe, A)
            display_set("Set B", universe, B)

        elif choice == "2":
            display_set("Union (A U B)", universe, union(A, B))

        elif choice == "3":
            display_set("Intersection (A n B)", universe, intersection(A, B))

        elif choice == "4":
            display_set("Complement of A", universe, complement(A))
            display_set("Complement of B", universe, complement(B))

        elif choice == "5":
            display_set("Difference (A - B)", universe, difference(A, B))

        elif choice == "6":
            display_set("Difference (B - A)", universe, difference(B, A))

        elif choice == "7":
            display_set("Algebraic Sum", universe, algebraic_sum(A, B))

        elif choice == "8":
            display_set("Algebraic Product", universe, algebraic_product(A, B))

        elif choice == "9":
            display_set("Bounded Sum", universe, bounded_sum(A, B))

        elif choice == "10":
            display_set("Bounded Difference (A - B)", universe, bounded_difference(A, B))
            display_set("Bounded Difference (B - A)", universe, bounded_difference(B, A))

        elif choice == "11":
            display_cartesian_product(universe, A, B)

        elif choice == "12":
            all_operations(universe, A, B)

        elif choice == "13":
            max_min_composition()

        elif choice == "14":
            max_product_composition()

        elif choice == "15":
            both_compositions()

        elif choice == "16":
            universe, A, B = input_sets()

        elif choice == "17":
            print("\nProgram terminated.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
