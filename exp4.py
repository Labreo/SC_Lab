import math
def sigmoid(net, lam):
    return 1 / (1 + math.exp(-lam * net))
def get_float(prompt):
    return float(input(prompt))
print("=== Error Back-Propagation Algorithm ===\n")
x1 = get_float("Enter x1: ")
x2 = get_float("Enter x2: ")
v13 = get_float("Enter v13: ")
v14 = get_float("Enter v14: ")
v23 = get_float("Enter v23: ")
v24 = get_float("Enter v24: ")
w35 = get_float("Enter w35: ")
w45 = get_float("Enter w45: ")
d = get_float("Enter desired output (d): ")
lam = get_float("Enter lambda: ")
eta = get_float("Enter learning rate (eta): ")
Emax = get_float("Enter maximum allowable error (Emax): ")
iteration = 0
E = float("inf")
while E > Emax:
    iteration += 1
    print(f"Iteration {iteration}")
    net3 = v13 * x1 + v23 * x2
    y3 = sigmoid(net3, lam)
    net4 = v14 * x1 + v24 * x2
    y4 = sigmoid(net4, lam)
    net5 = w35 * y3 + w45 * y4
    y5 = sigmoid(net5, lam)
    print(f"net3 = {net3:.5f}   y3 = {y3:.5f}")
    print(f"net4 = {net4:.5f}   y4 = {y4:.5f}")
    print(f"net5 = {net5:.5f}   y5 (output) = {y5:.5f}")
    E = 0.5 * (d - y5) ** 2
    print(f"Error E = {E:.5f}")
    delta5 = (d - y5) * (1 - y5) * y5
    f3_prime = (1 - y3) * y3
    f4_prime = (1 - y4) * y4
    delta3 = w35 * delta5 * f3_prime
    delta4 = w45 * delta5 * f4_prime
    print(f"delta5 = {delta5:.5f}")
    print(f"delta3 = {delta3:.5f}")
    print(f"delta4 = {delta4:.5f}")
    w35 = w35 + eta * delta5 * y3
    w45 = w45 + eta * delta5 * y4
    print(f"Updated w35 = {w35:.5f}")
    print(f"Updated w45 = {w45:.5f}")
    v13 = v13 + eta * delta3 * x1
    v23 = v23 + eta * delta3 * x2
    v14 = v14 + eta * delta4 * x1
    v24 = v24 + eta * delta4 * x2
    print(f"Updated v13 = {v13:.5f}")
    print(f"Updated v23 = {v23:.5f}")
    print(f"Updated v14 = {v14:.5f}")
    print(f"Updated v24 = {v24:.5f}")
    print()
    if E <= Emax:
        print(f"Error {E:.5f} <= Emax {Emax:.5f}. Training stopped.\n")
        break
print()
print(f"Final output y5  : {y5:.5f}")
print(f"Final error E    : {E:.5f}")
print(f"Final weights:")
print(f"  v13 = {v13:.5f}, v14 = {v14:.5f}")
print(f"  v23 = {v23:.5f}, v24 = {v24:.5f}")
print(f"  w35 = {w35:.5f}, w45 = {w45:.5f}")