import numpy as np
import random

def objective_function(x):
    return x * np.sin(10 * np.pi * x) + 2

def decode_chromosome(chromosome, x_min, x_max):
    decimal = int("".join(map(str, chromosome)), 2)
    x = x_min + (decimal / (2 ** len(chromosome) - 1)) * (x_max - x_min)
    return decimal, x

def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return random.choice(population)
    probabilities = [f / total_fitness for f in fitness_values]
    cum_probs = np.cumsum(probabilities)
    r = random.random()
    idx = np.searchsorted(cum_probs, r)
    idx = min(idx, len(population) - 1)
    return population[idx]

def single_point_crossover(parent1, parent2, pc):
    if random.random() < pc:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1[:], parent2[:]

def bit_flip_mutation(chromosome, pm):
    mutated = chromosome[:]
    for i in range(len(mutated)):
        if random.random() < pm:
            mutated[i] = 1 - mutated[i]
    return mutated

print("\n================================")
print("Genetic Algorithm Optimization")
print("Maximize: f(x) = x * sin(10*pi*x) + 2")
print("================================")

pop_size = int(input("Enter population size: ").strip() or 20)
chrom_len = int(input("Enter chromosome length (bits): ").strip() or 10)
generations = int(input("Enter number of generations: ").strip() or 50)
x_min = float(input("Enter lower bound of x: ").strip() or -1.0)
x_max = float(input("Enter upper bound of x: ").strip() or 2.0)
pc = float(input("Enter crossover probability: ").strip() or 0.8)
pm = float(input("Enter mutation probability: ").strip() or 0.05)

population = []
for _ in range(pop_size):
    chromosome = [random.randint(0, 1) for _ in range(chrom_len)]
    population.append(chromosome)

decoded_info = [decode_chromosome(ind, x_min, x_max) for ind in population]
x_values = [item[1] for item in decoded_info]
fitness_values = [objective_function(x) for x in x_values]

total_fit = sum(fitness_values)
probs = [f / total_fit for f in fitness_values] if total_fit > 0 else [1.0 / pop_size] * pop_size
cum_probs = np.cumsum(probs)

print("\n--- Initial Population (Generation 1) ---")
print("No.  Chromosome   Decimal     x       Fitness   Selection Prob  Cumulative Prob")
print("-------------------------------------------------------------------------------")
for i in range(pop_size):
    chrom_str = "".join(map(str, population[i]))
    dec_val, x_val = decoded_info[i]
    fit_val = fitness_values[i]
    prob_val = probs[i]
    cum_val = cum_probs[i]
    print(f"{i+1:2d}   {chrom_str}   {dec_val:4d}    {x_val:7.4f}   {fit_val:7.4f}      {prob_val:7.4f}          {cum_val:7.4f}")

print("\n--- Generation Progress ---")
print("Gen      Best Chromosome    Best x    Best Fitness    Avg Fitness")
print("-----------------------------------------------------------------")

best_overall_chrom = None
best_overall_dec = None
best_overall_x = None
best_overall_fitness = float("-inf")

for gen in range(1, generations + 1):
    decoded_info = [decode_chromosome(ind, x_min, x_max) for ind in population]
    x_values = [item[1] for item in decoded_info]
    fitness_values = [objective_function(x) for x in x_values]

    best_idx = int(np.argmax(fitness_values))
    gen_best_fitness = fitness_values[best_idx]
    gen_best_x = x_values[best_idx]
    gen_best_dec = decoded_info[best_idx][0]
    gen_best_chrom = population[best_idx][:]
    avg_fitness = float(np.mean(fitness_values))

    if gen_best_fitness > best_overall_fitness:
        best_overall_fitness = gen_best_fitness
        best_overall_x = gen_best_x
        best_overall_dec = gen_best_dec
        best_overall_chrom = gen_best_chrom[:]

    best_chrom_str = "".join(map(str, gen_best_chrom))
    print(f"{gen:3d}        {best_chrom_str}     {gen_best_x:7.4f}      {gen_best_fitness:7.4f}        {avg_fitness:7.4f}")

    new_population = []
    while len(new_population) < pop_size:
        p1 = roulette_wheel_selection(population, fitness_values)
        p2 = roulette_wheel_selection(population, fitness_values)
        c1, c2 = single_point_crossover(p1, p2, pc)
        c1 = bit_flip_mutation(c1, pm)
        c2 = bit_flip_mutation(c2, pm)
        new_population.append(c1)
        if len(new_population) < pop_size:
            new_population.append(c2)

    new_decoded = [decode_chromosome(ind, x_min, x_max) for ind in new_population]
    new_fitness = [objective_function(item[1]) for item in new_decoded]

    if gen_best_fitness > max(new_fitness):
        worst_idx = int(np.argmin(new_fitness))
        new_population[worst_idx] = gen_best_chrom[:]

    population = new_population

final_decoded = [decode_chromosome(ind, x_min, x_max) for ind in population]
final_fitness = [objective_function(item[1]) for item in final_decoded]

print(f"\n--- Final Population (Generation {generations}) ---")
print("No.  Chromosome   Decimal     x       Fitness")
print("------------------------------------------------")
for i in range(pop_size):
    chrom_str = "".join(map(str, population[i]))
    dec_val, x_val = final_decoded[i]
    fit_val = final_fitness[i]
    print(f"{i+1:2d}   {chrom_str}   {dec_val:4d}    {x_val:7.4f}   {fit_val:7.4f}")

optimal_chrom_str = "".join(map(str, best_overall_chrom))

print("\n================================")
print("Optimization Completed")
print("================================")
print(f"Optimal Chromosome: {optimal_chrom_str}")
print(f"Decimal Value: {best_overall_dec}")
print(f"Optimal x: {best_overall_x:.6f}")
print(f"Maximum f(x): {best_overall_fitness:.6f}")
