import random
 
POP_SIZE = 20
BITS = 10                
GENERATIONS = 50
MUTATION_RATE = 0.1
NUM_CITIES = 10

ADJ_MATRIX = [
    [0,  14, 12, 18, 25,31, 9 ,15 ,22 ,19],
    [14, 0, 11, 20, 28, 17 ,13 ,24,16,21],
    [12, 11, 0,  15, 19, 23,27,10,14,26],
    [18, 20, 15, 0,  13,16 , 22, 29, 12,17],
    [25, 28, 19, 13, 0 ,14 , 21, 18, 11, 15],
    [31, 17, 23,  16, 14, 0,19,25,20,12],
    [9, 13, 27, 22, 21, 19 , 0, 16, 24, 18],
    [15, 24, 10, 29, 18,25 ,16 ,0,13,22],
    [22, 16, 14, 12, 11,20 , 24, 13, 0,14],
    [19, 21, 26, 17, 15,12 , 18, 22, 14,0]

]

def decode(chromosome):
    keys = [int(chromosome[i]) for i in range(NUM_CITIES)]
    tour = [city for _, city in sorted(zip(keys, range(NUM_CITIES)))]
    return tour

def tour_distance(chromosome):
    tour = decode(chromosome)
    dist = 0
    for i in range(NUM_CITIES):
        u = tour[i]
        v = tour[(i + 1) % NUM_CITIES]  
        dist += ADJ_MATRIX[u][v]
    return dist

def fitness(chromosome):
    return 1000.0 / tour_distance(chromosome)


def create_population():
    population = []
    for _ in range(POP_SIZE):
        chromosome = "".join(random.choice("01") for _ in range(BITS))
        population.append(chromosome)
    return population


def roulette_selection(population):
    total_fit = sum(fitness(c) for c in population)
    pick = random.uniform(0, total_fit)
    current = 0
    for c in population:
        current += fitness(c)
        if current >= pick:
            return c
    return population[-1]

def crossover(p1, p2):
    point = random.randint(1, BITS - 1)
    c1 = p1[:point] + p2[point:]
    c2 = p2[:point] + p1[point:]
    return c1, c2, point


def mutate(chromosome):
    bits = list(chromosome)
    flipped = []
    for i in range(BITS):
        if random.random() < MUTATION_RATE:
            bits[i] = "1" if bits[i] == "0" else "0"
            flipped.append(i)
    return "".join(bits), flipped

population = create_population()
best_chromosome = max(population, key=fitness)
best_fitness = fitness(best_chromosome)

print("INITIAL POPULATION")
for i, c in enumerate(population, 1):
    print(f"{i:2d}: {c} | Tour: {decode(c)} | Distance: {tour_distance(c)} | Fitness: {fitness(c):.4f}")

for gen in range(1, GENERATIONS + 1):
    print(f"\n")
    print(f"GENERATION {gen}")
    print(f"")

    current_best = max(population, key=fitness)
    current_fitness = fitness(current_best)

    if current_fitness > best_fitness:
        best_chromosome = current_best
        best_fitness = current_fitness

    new_population = [current_best]

    for pair in range(1, (POP_SIZE // 2) + 1):
        parent1 = roulette_selection(population)
        parent2 = roulette_selection(population)

        print(f"\nPair {pair} - SELECTION")
        print(f"Parent 1: {parent1} (Tour: {decode(parent1)}, Dist: {tour_distance(parent1)})")
        print(f"Parent 2: {parent2} (Tour: {decode(parent2)}, Dist: {tour_distance(parent2)})")

        child1, child2, pt = crossover(parent1, parent2)
        print("CROSSOVER")
        print(f"Crossover point: {pt}")
        print(f"Child 1 before mutation: {child1}")
        print(f"Child 2 before mutation: {child2}")

        child1_mut, flip1 = mutate(child1)
        child2_mut, flip2 = mutate(child2)
        print("MUTATION")
        print(f"Child 1: {child1_mut} Flipped bits: {flip1}")
        print(f"Child 2: {child2_mut} Flipped bits: {flip2}")

        new_population.append(child1_mut)
        if len(new_population) < POP_SIZE:
            new_population.append(child2_mut)

    population = new_population

    print(f"\n Generation {gen} Best ")
    print(f"Best Chromosome : {best_chromosome}")
    print(f"Best Tour       : {decode(best_chromosome)} -> {decode(best_chromosome)[0]}")
    print(f"Minimum Distance: {tour_distance(best_chromosome)}")
    print(f"Maximum Fitness : {best_fitness:.4f}")

best_tour = decode(best_chromosome)
print("\nFINAL RESULT")
print("Best chromosome:", best_chromosome)
print("Best TSP Tour  :", best_tour + [best_tour[0]])
print("Minimum distance:", tour_distance(best_chromosome))
print("Maximum fitness:", round(best_fitness, 6))