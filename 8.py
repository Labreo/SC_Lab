def read_value(msg):
    while True:
        try:
            val = float(eval(input(msg), {"__builtins__": {}}, {}))
            if 0 <= val <= 1:
                return val
            print("Membership value must be between 0 and 1.")
        except:
            print("Enter valid value like 1/2, 3/4 or 0.75.")


def input_sets():
    print("\nEnter Fuzzy Set Details")
    n = int(input("Enter number of elements in universe: "))
    universe = [input(f"Element {i + 1}: ") for i in range(n)]
    print("\nEnter membership values for Set A:")
    A = [read_value(f"A({u}) = ") for u in universe]
    print("\nEnter membership values for Set B:")
    B = [read_value(f"B({u}) = ") for u in universe]
    return universe, A, B


def display_set(name, universe, values):
    print(f"\n{name}\n" + "-" * 35)
    for u, v in zip(universe, values):
        print(f"{u} : {v:.3f}")
    print("Fuzzy Set Notation:", "{" + ", ".join(f"{v:.3f}/{u}" for u, v in zip(universe, values)) + "}")


def display_matrix(name, matrix, row_labels=None, col_labels=None):
    print(f"\n{name}\n" + "-" * 45)
    if col_labels:
        print("       " + "  ".join(f"{str(c):>7}" for c in col_labels))
    for i, row in enumerate(matrix):
        r_str = "  ".join(f"{v:7.3f}" for v in row)
        print(f"{str(row_labels[i]):>5} : {r_str}" if row_labels else f"  {r_str}")


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
    if method == "min":
        return [[min(a, b) for b in B] for a in A]
    return [[round(a * b, 4) for b in B] for a in A]


def display_cartesian_product(universe, A, B):
    print("\n========== CARTESIAN PRODUCT OF FUZZY SETS ==========")
    display_matrix("Cartesian Product using Min (A x B)", cartesian_product(A, B, "min"), universe, universe)
    display_matrix("Cartesian Product using Algebraic Product (A . B)", cartesian_product(A, B, "prod"), universe, universe)


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
    left1, right1 = complement(union(A, B)), intersection(complement(A), complement(B))
    left2, right2 = complement(intersection(A, B)), union(complement(A), complement(B))
    display_set("Complement of Union [!(A U B)]", universe, left1)
    display_set("Intersection of Complements [!A n !B]", universe, right1)
    print("First De Morgan's Law Verified:", all(abs(l - r) < 1e-4 for l, r in zip(left1, right1)))
    display_set("Complement of Intersection [!(A n B)]", universe, left2)
    display_set("Union of Complements [!A U !B]", universe, right2)
    print("Second De Morgan's Law Verified:", all(abs(l - r) < 1e-4 for l, r in zip(left2, right2)))


def input_relation(name):
    print(f"\nEnter details for Relation {name}")
    r, c = int(input("Enter number of rows: ")), int(input("Enter number of columns: "))
    mat = []
    for i in range(r):
        print(f"Enter values for row {i + 1} ({c} values):")
        mat.append([read_value(f"Enter {name}[{i+1}][{j+1}]: ") for j in range(c)])
    return mat


def compose(R, S, method):
    rows, cols, common = len(R), len(S[0]), len(S)
    res = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if method == "min":
                val = max(min(R[i][k], S[k][j]) for k in range(common))
            else:
                val = max(R[i][k] * S[k][j] for k in range(common))
            row.append(round(val, 4))
        res.append(row)
    return res


def max_min_composition():
    print("\n========== MAX-MIN COMPOSITION (R o S) ==========")
    R, S = input_relation("R"), input_relation("S")
    if len(R[0]) != len(S):
        print(f"\nComposition not possible. Columns of R ({len(R[0])}) != rows of S ({len(S)}).")
        return
    display_matrix("Relation R", R)
    display_matrix("Relation S", S)
    display_matrix("Max-Min Composition (R o S)", compose(R, S, "min"))


def max_product_composition():
    print("\n========== MAX-PRODUCT COMPOSITION (R . S) ==========")
    R, S = input_relation("R"), input_relation("S")
    if len(R[0]) != len(S):
        print(f"\nComposition not possible. Columns of R ({len(R[0])}) != rows of S ({len(S)}).")
        return
    display_matrix("Relation R", R)
    display_matrix("Relation S", S)
    display_matrix("Max-Product Composition (R . S)", compose(R, S, "prod"))


def both_compositions():
    print("\n========== BOTH COMPOSITIONS (MAX-MIN & MAX-PRODUCT) ==========")
    R, S = input_relation("R"), input_relation("S")
    if len(R[0]) != len(S):
        print(f"\nComposition not possible. Columns of R ({len(R[0])}) != rows of S ({len(S)}).")
        return
    display_matrix("Relation R", R)
    display_matrix("Relation S", S)
    display_matrix("Max-Min Composition (R o S)", compose(R, S, "min"))
    display_matrix("Max-Product Composition (R . S)", compose(R, S, "prod"))


def main():
    print("========== FUZZY SET OPERATIONS & COMPOSITIONS ==========")
    universe, A, B = input_sets()
    menu = """
============== MAIN MENU ==============
1. Display Sets A and B
2. Union (Maximum)
3. Intersection (Minimum)
4. Complement of A and B
5. Difference (A - B)
6. Difference (B - A)
7. Algebraic Sum
8. Algebraic Product
9. Bounded Sum
10. Bounded Difference
11. Cartesian Product (Min & Product)
12. All Set Operations & De Morgan's Laws
13. Max-Min Composition of Relations
14. Max-Product Composition of Relations
15. Both Compositions (Max-Min & Max-Product)
16. Enter New Sets
17. Exit"""
    while True:
        print(menu)
        ch = input("\nEnter your choice: ").strip()
        if ch == '1':
            display_set("Set A", universe, A)
            display_set("Set B", universe, B)
        elif ch == '2':
            display_set("Union (A U B)", universe, union(A, B))
        elif ch == '3':
            display_set("Intersection (A n B)", universe, intersection(A, B))
        elif ch == '4':
            display_set("Complement of A", universe, complement(A))
            display_set("Complement of B", universe, complement(B))
        elif ch == '5':
            display_set("Difference (A - B)", universe, difference(A, B))
        elif ch == '6':
            display_set("Difference (B - A)", universe, difference(B, A))
        elif ch == '7':
            display_set("Algebraic Sum", universe, algebraic_sum(A, B))
        elif ch == '8':
            display_set("Algebraic Product", universe, algebraic_product(A, B))
        elif ch == '9':
            display_set("Bounded Sum", universe, bounded_sum(A, B))
        elif ch == '10':
            display_set("Bounded Difference (A - B)", universe, bounded_difference(A, B))
            display_set("Bounded Difference (B - A)", universe, bounded_difference(B, A))
        elif ch == '11':
            display_cartesian_product(universe, A, B)
        elif ch == '12':
            all_operations(universe, A, B)
        elif ch == '13':
            max_min_composition()
        elif ch == '14':
            max_product_composition()
        elif ch == '15':
            both_compositions()
        elif ch == '16':
            universe, A, B = input_sets()
        elif ch == '17':
            print("\nProgram terminated.")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == '__main__':
    main()
