import numpy as np

n = int(input("Enter number of input vectors: "))
m = int(input("Enter number of elements in each vector: "))

print("\nEnter initial weight matrix:")
w = np.array(list(map(float, input("W1: ").split())))

x = []

print("\nEnter input vectors:")

for i in range(n):
    values = list(map(float, input(f"X{i+1}: ").split()))
    x.append(values)

x = np.array(x)

print("\nEnter desired values:")

d = []

for i in range(n):
    d.append(float(input(f"d{i+1}: ")))

c = float(input("\nEnter learning rate c: "))

iteration = 1

while True:

    print("\n================================")
    

    changes = 0

    for i in range(n):

        xi = x[i]

        print(f"\n--- X{i+1} ---")

        print("W =", np.array2string(
            w,
            formatter={'float_kind': lambda x: f"{x:.2f}"}
        ))

        print("X =", np.array2string(
            xi,
            formatter={'float_kind': lambda x: f"{x:.2f}"}
        ))

        net = np.dot(w, xi)

        print(f"net{i+1} = W{i+1}ᵀ X{i+1}")
        print(f"net{i+1} = {net:.2f}")

        if net >= 0:
            y = 1
        else:
            y = -1

        print(f"sgn(net{i+1}) =", y)
        print(f"d{i+1} =", d[i])

        if y == d[i]:

            print("sgn(net) = d")
            print("No change in weight")

        else:

            print("sgn(net) != d")

            if d[i] == 1:
                w_new = w + 2 * c * xi
                print(f"W{i+2} = W{i+1} + 2cX{i+1}")
            else:
                w_new = w - 2 * c * xi
                print(f"W{i+2} = W{i+1} - 2cX{i+1}")

            print("New W =", np.array2string(
                w_new,
                formatter={'float_kind': lambda x: f"{x:.2f}"}
            ))

            w = w_new
            changes += 1

    if changes == 0:

        print("\n================================")
        print("Training Completed")
        print("================================")

        print("Final Weight Matrix =",
              np.array2string(
                  w,
                  formatter={'float_kind': lambda x: f"{x:.2f}"}
              ))

        break

    iteration += 1