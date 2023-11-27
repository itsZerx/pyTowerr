import pygad
import random


class GeneticAlgorithm:
    def __init__(self, num_generations=50, num_parents_mating=4, sol_per_pop=10, num_genes=2, simulated_enemy_count=10):
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.sol_per_pop = sol_per_pop
        self.num_genes = num_genes
        self.simulated_enemy_count = simulated_enemy_count

        self.ga_instance = self.setup_ga()

    def fitness_function(self, solution):
        hits = 0
        for _ in range(self.simulated_enemy_count):
            if self.tower_hits_enemy(solution):
                hits += 1
        return hits

    def tower_hits_enemy(self, solution):
        target_selection_range, accuracy = solution
        hit_chance = random.random()
        return hit_chance < accuracy

    def setup_ga(self):
        return pygad.GA(num_generations=self.num_generations,
                        num_parents_mating=self.num_parents_mating,
                        fitness_func=self.fitness_function,
                        sol_per_pop=self.sol_per_pop,
                        num_genes=self.num_genes,
                        init_range_low=0.1,
                        init_range_high=1,
                        mutation_percent_genes=10)

    def run(self):
        self.ga_instance.run()

    def get_best_solution(self):
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        return solution, solution_fitness
