import random
import math

POP_SIZE = 8
BITS = 10
GENERATIONS = 5
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.01

# Generate random chromosome
def create_chromosome():
    return ''.join(random.choice('01') for _ in range(BITS))

# Convert binary to normalized x
def decode(ch):
    return int(ch, 2) / 1023

# Fitness function
def fitness(ch):
    x = decode(ch)
    return x * math.sin(10 * math.pi * x) + 2

# Roulette wheel selection
def roulette_wheel_selection(population):
    values = [fitness(ch) for ch in population]
    total = sum(values)
    pick = random.uniform(0, total)
    current = 0

    for ch, value in zip(population, values):
        current += value
        if current >= pick:
            return ch

    return population[-1]

# Single-point crossover
def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, BITS - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
        return c1, c2, point

    return p1, p2, None

# Mutation
def mutation(ch):
    result = ''
    changes = []

    for i, bit in enumerate(ch):
        if random.random() < MUTATION_RATE:
            new_bit = '1' if bit == '0' else '0'
            changes.append(f"{i + 1}:{bit}->{new_bit}")
            result += new_bit
        else:
            result += bit

    return result, ', '.join(changes) if changes else 'None'

# Initial population
population = [create_chromosome() for _ in range(POP_SIZE)]

print("INITIAL POPULATION")
for i, ch in enumerate(population, 1):
    print(f"{i}. {ch} | Fitness: {fitness(ch):.4f}")

# Run 5 generations
for generation in range(1, GENERATIONS + 1):
    new_population = []
    results = []
    child_no = 1

    while len(new_population) < POP_SIZE:
        # Selection
        p1 = roulette_wheel_selection(population)
        p2 = roulette_wheel_selection(population)

        # Crossover
        c1, c2, point = crossover(p1, p2)

        # Mutation
        m1, changes1 = mutation(c1)
        m2, changes2 = mutation(c2)

        children = [
            (p1, p2, c1, m1, changes1),
            (p1, p2, c2, m2, changes2)
        ]

        for parent1, parent2, cross_child, final_child, changes in children:
            if len(new_population) >= POP_SIZE:
                break

            new_population.append(final_child)

            crossover_result = (
                f"Point {point}: {cross_child}"
                if point is not None
                else f"Skipped: {cross_child}"
            )

            results.append(
                (child_no, parent1, parent2, crossover_result,
                 changes, final_child, fitness(final_child))
            )
            child_no += 1

    population = new_population

    print(f"\nGENERATION {generation}")
    for no, p1, p2, cross, mut, sol, fit in results:
        print(f"\nSolution {no}")
        print(f"Selection: {p1}, {p2}")
        print(f"Crossover: {cross}")
        print(f"Mutation: {mut}")
        print(f"Final Solution: {sol}")
        print(f"Fitness: {fit:.4f}")

    best = max(population, key=fitness)
    print(f"\nBest: {best} | x = {decode(best):.6f} "
          f"| Fitness = {fitness(best):.4f}")

# Final best solution
best = max(population, key=fitness)

print("\nFINAL BEST SOLUTION")
print("Chromosome:", best)
print("Decimal value:", int(best, 2))
print("x =", decode(best))
print("Fitness =", fitness(best))