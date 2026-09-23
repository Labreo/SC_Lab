import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoid_derivative(output):
    return output * (1.0 - output)

n = int(input("Enter number of training patterns: "))
num_in = int(input("Enter number of input features: "))
num_hid = int(input("Enter number of hidden neurons: "))
num_out = int(input("Enter number of output neurons: "))

print("\nEnter initial Input-to-Hidden weights (V):")
v = []
for i in range(num_in):
    row = list(map(float, input(f"V row {i+1}: ").split()))
    v.append(row)
v = np.array(v, dtype=float)

print("\nEnter initial Hidden-to-Output weights (W):")
w = []
for i in range(num_hid):
    row = list(map(float, input(f"W row {i+1}: ").split()))
    w.append(row)
w = np.array(w, dtype=float)

x = []
print("\nEnter input patterns:")
for i in range(n):
    values = list(map(float, input(f"X{i+1}: ").split()))
    x.append(values)
x = np.array(x, dtype=float)

d = []
print("\nEnter desired target outputs:")
for i in range(n):
    targets = list(map(float, input(f"D{i+1}: ").split()))
    d.append(targets)
d = np.array(d, dtype=float)

c = float(input("\nEnter learning rate c: "))
epochs = int(input("Enter number of epochs to train: "))

for epoch in range(1, epochs + 1):
    print(f"\n--- Epoch {epoch} ---")
    total_epoch_error = 0.0

    for i in range(n):
        xi = x[i:i+1]
        di = d[i:i+1]

        print(f"\nPattern X{i+1}:")
        print("X =", xi[0])
        print("Target D =", di[0])

        net_h = np.dot(xi, v)
        y = sigmoid(net_h)
        print("net_hidden =", np.round(net_h[0], 4))
        print("Hidden Output Y =", np.round(y[0], 4))

        net_o = np.dot(y, w)
        o = sigmoid(net_o)
        print("net_output =", np.round(net_o[0], 4))
        print("Actual Output O =", np.round(o[0], 4))

        error = di - o
        pattern_mse = 0.5 * np.sum(error ** 2)
        total_epoch_error += pattern_mse
        print("Error =", np.round(error[0], 4))
        print("Pattern MSE =", round(pattern_mse, 6))

        delta_o = error * sigmoid_derivative(o)
        print("Output Delta =", np.round(delta_o[0], 4))

        error_h = np.dot(delta_o, w.T)
        delta_h = error_h * sigmoid_derivative(y)
        print("Hidden Delta =", np.round(delta_h[0], 4))

        delta_w = c * np.dot(y.T, delta_o)
        w_new = w + delta_w
        print("Updated W:\n", np.round(w_new, 4))

        delta_v = c * np.dot(xi.T, delta_h)
        v_new = v + delta_v
        print("Updated V:\n", np.round(v_new, 4))

        w = w_new
        v = v_new

    avg_error = total_epoch_error / n
    print(f"\nEpoch {epoch} Average Error: {round(avg_error, 6)}")

print("\nFinal Input-to-Hidden Weights (V):")
print(np.round(v, 4))
print("\nFinal Hidden-to-Output Weights (W):")
print(np.round(w, 4))