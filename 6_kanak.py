import math
import random

SWARM_SIZE = 20
ITERATIONS = 10
W = 0.5
C1 = 1.5
C2 = 1.5
X_MIN = 0.0
X_MAX = 1.0
V_MIN = -0.1
V_MAX = 0.1


def fitness(x):
    return x * math.sin(10 * math.pi * x) + 2


particles = [random.uniform(X_MIN, X_MAX) for _ in range(SWARM_SIZE)]
velocities = [random.uniform(V_MIN, V_MAX) for _ in range(SWARM_SIZE)]

pbest = list(particles)
pbest_fitness = [fitness(x) for x in pbest]

gbest = pbest[pbest_fitness.index(max(pbest_fitness))]
gbest_fitness = max(pbest_fitness)

print("INITIAL SWARM")
for i in range(SWARM_SIZE):
    print(
        f"Particle {i + 1}: x = {round(particles[i], 6)}, Fitness = {round(pbest_fitness[i], 4)}"
    )

for iteration in range(1, ITERATIONS + 1):
    print(f"\n========== ITERATION {iteration} ==========")

    for i in range(SWARM_SIZE):
        r1 = random.random()
        r2 = random.random()

        velocities[i] = (
            W * velocities[i]
            + C1 * r1 * (pbest[i] - particles[i])
            + C2 * r2 * (gbest - particles[i])
        )
        velocities[i] = max(V_MIN, min(V_MAX, velocities[i]))

        particles[i] += velocities[i]
        particles[i] = max(X_MIN, min(X_MAX, particles[i]))

        current_fit = fitness(particles[i])

        if current_fit > pbest_fitness[i]:
            pbest[i] = particles[i]
            pbest_fitness[i] = current_fit

            if current_fit > gbest_fitness:
                gbest = particles[i]
                gbest_fitness = current_fit

        print(
            f"Particle {i + 1}: x = {round(particles[i], 6)}, v = {round(velocities[i], 6)}, Fitness = {round(current_fit, 6)}"
        )

    print(f"Current Best x: {round(gbest, 6)}")
    print(f"Current Best Fitness: {round(gbest_fitness, 6)}")

print("\n========== FINAL RESULT ==========")
print("Best particle (x):", gbest)
print("Best x:", round(gbest, 6))
print("Maximum fitness:", gbest_fitness)