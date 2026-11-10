import random
import math

def objective_function(x):
    return x * math.sin(10 * math.pi * x) + 2.0

NUM_PARTICLES = 20
ITERATIONS = 5
C1 = 2.0 
C2 = 2.0 
X_MIN = -1.0
X_MAX = 2.0
V_MIN = -0.5  
V_MAX = 0.5

class Particle:
    def __init__(self):
        self.position = random.uniform(X_MIN, X_MAX)
        self.velocity = random.uniform(V_MIN, V_MAX)
        
        self.pbest_position = self.position
        self.pbest_value = objective_function(self.position)

def pso_maximize():
    swarm = [Particle() for _ in range(NUM_PARTICLES)]
    gbest_position = swarm[0].position
    gbest_value = swarm[0].pbest_value
    
    for particle in swarm:
        if particle.pbest_value > gbest_value:
            gbest_value = particle.pbest_value
            gbest_position = particle.position

    print("INITIAL SWARM STATE: ")
    print(f"Initial Global Best: x = {gbest_position:.4f}, f(x) = {gbest_value:.4f}")

    for t in range(ITERATIONS):
        print(f"\nITERATION {t + 1} : ")
        
        for particle in swarm:
            r1 = random.random()
            r2 = random.random()
            
            cognitive_component = C1 * r1 * (particle.pbest_position - particle.position)
            social_component = C2 * r2 * (gbest_position - particle.position)
            particle.velocity = particle.velocity + cognitive_component + social_component
        
            particle.velocity = max(min(particle.velocity, V_MAX), V_MIN)
            particle.position = particle.position + particle.velocity
            particle.position = max(min(particle.position, X_MAX), X_MIN)
            
            current_fitness = objective_function(particle.position)
            
            if current_fitness > particle.pbest_value:
                particle.pbest_value = current_fitness
                particle.pbest_position = particle.position
                
            if current_fitness > gbest_value:
                gbest_value = current_fitness
                gbest_position = particle.position
                
        for i, particle in enumerate(swarm):
            print(f"Particle {i + 1:02d}: Particle Position x_t = {particle.position: .6f}, Local Best x = {particle.pbest_position:.6f}, f(x) = {particle.pbest_value:.6f}")
            
        print(f"Iteration {t + 1} Global Best: x = {gbest_position:.6f}, f(x) = {gbest_value:.6f}")

    print("\n          FINAL BEST SOLUTION            ")
    print(f"Best x Value       : {gbest_position:.6f}")
    print(f"Max Fitness (f(x)) : {gbest_value:.6f}")

if __name__ == "__main__":
    pso_maximize()