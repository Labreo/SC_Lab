import random

POP_SIZE = 20
BITS = 10
GENERATIONS = 5
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.05

ADJ_MATRIX = [
    [0, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    [10, 0, 35, 25, 18, 40, 20, 15, 30, 22],
    [15, 35, 0, 30, 28, 12, 45, 22, 19, 34],
    [20, 25, 30, 0, 14, 26, 17, 33, 41, 16],
    [25, 18, 28, 14, 0, 31, 29, 27, 38, 13],
    [30, 40, 12, 26, 31, 0, 24, 36, 18, 28],
    [35, 20, 45, 17, 29, 24, 0, 19, 32, 21],
    [40, 15, 22, 33, 27, 36, 19, 0, 25, 18],
    [45, 30, 19, 41, 38, 18, 32, 25, 0, 15],
    [50, 22, 34, 16, 13, 28, 21, 18, 15, 0]
]

def create_chromosome():
    ch = list(range(BITS))
    random.shuffle(ch)
    return ch

def calculate_distance(ch):
    dist = 0
    for i in range(len(ch)):
        dist += ADJ_MATRIX[ch[i]][ch[(i + 1) % len(ch)]]
    return dist

def fitness(ch):
    return 1 / calculate_distance(ch)

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

def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, BITS - 1)
        c1 = p1[:point] + [x for x in p2 if x not in p1[:point]]
        c2 = p2[:point] + [x for x in p1 if x not in p2[:point]]
        return c1, c2, point
    return p1[:], p2[:], None

def mutation(ch):
    result = ch[:]
    changes = []
    for i in range(len(result)):
        if random.random() < MUTATION_RATE:
            j = random.randint(0, len(result) - 1)
            result[i], result[j] = result[j], result[i]
            changes.append(f"{i + 1}<->{j + 1}")
    return result, ', '.join(changes) if changes else 'None'

population = [create_chromosome() for _ in range(POP_SIZE)]

print("INITIAL POPULATION")
for i, ch in enumerate(population, 1):
    print(f"{i}. {ch} | Distance: {calculate_distance(ch)} | Fitness: {fitness(ch):.6f}")

for generation in range(1, GENERATIONS + 1):
    new_population = []
    results = []
    child_no = 1

    while len(new_population) < POP_SIZE:
        p1 = roulette_wheel_selection(population)
        p2 = roulette_wheel_selection(population)

        c1, c2, point = crossover(p1, p2)

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
        print(f"Distance: {calculate_distance(sol)}")
        print(f"Fitness: {fit:.6f}")

    best = max(population, key=fitness)
    print(f"\nBest: {best} | Distance = {calculate_distance(best)} | Fitness = {fitness(best):.6f}")

best = max(population, key=fitness)

print("\nFINAL BEST SOLUTION")
print("Best Route:", best)
print("Total Distance:", calculate_distance(best))
print(f"Fitness: {fitness(best):.6f}")

