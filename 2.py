def single_neuron_gate(gate_name):
    print(f"\nSelected Gate: {gate_name}")
    if gate_name == "AND":
        weights = [1, 1, 1]
        threshold = 3
    elif gate_name == "NAND":
        weights = [-1, -1, -1]
        threshold = -2
    elif gate_name == "OR":
        weights = [1, 1, 1]
        threshold = 1
    elif gate_name == "NOR":
        weights = [-1, -1, -1]
        threshold = 0

    print(f"Weights: {weights}")
    print(f"Threshold: {threshold}")

    print("\nTruth Table")
    print("x1 x2 x3 | Output")
    print("------------------")
    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                weighted_sum = x1 * weights[0] + x2 * weights[1] + x3 * weights[2]
                output = 1 if weighted_sum >= threshold else 0
                print(f"{x1}  {x2}  {x3}  | {output}")

    while True:
        print("\nEnter Input Values")
        x1 = int(input("Enter x1 (0 or 1): "))
        x2 = int(input("Enter x2 (0 or 1): "))
        x3 = int(input("Enter x3 (0 or 1): "))
        weighted_sum = x1 * weights[0] + x2 * weights[1] + x3 * weights[2]
        output = 1 if weighted_sum >= threshold else 0
        print(f"Weighted Sum: {weighted_sum}")
        print(f"{gate_name} Output: {output}")

        choice = input("\nWant to continue with this gate?: ").lower()
        if choice == "no":
            break


def xor_gate():
    print("\nSelected Gate: XOR")
    print("\nXOR uses multiple MP neurons.")

    print("\nTruth Table")
    print("x1 x2 x3 | Output")
    print("------------------")
    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                count = x1 + x2 + x3
                if count == 1 or count == 3:
                    output = 1
                else:
                    output = 0
                print(f"{x1}  {x2}  {x3}  | {output}")

    while True:
        print("\nEnter Input Values")
        x1 = int(input("Enter x1 (0 or 1): "))
        x2 = int(input("Enter x2 (0 or 1): "))
        x3 = int(input("Enter x3 (0 or 1): "))

        count = x1 + x2 + x3
        if count == 1 or count == 3:
            output = 1
        else:
            output = 0
        print(f"XOR Output: {output}")

        choice = input("\nWant to continue with XOR?: ").lower()
        if choice == "no":
            break


while True:
    print("\nMcCulloch-Pitts Neuron Model")
    print("1. AND")
    print("2. NAND")
    print("3. OR")
    print("4. NOR")
    print("5. XOR")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        single_neuron_gate("AND")
    elif choice == "2":
        single_neuron_gate("NAND")
    elif choice == "3":
        single_neuron_gate("OR")
    elif choice == "4":
        single_neuron_gate("NOR")
    elif choice == "5":
        xor_gate()
    elif choice == "6":
        print("Exiting")
        break
    else:
        print("Invalid choice")