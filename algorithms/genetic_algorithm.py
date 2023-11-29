import random


class GeneticAlgorithm:
    def __init__(self):
        self.num_generations = None
        self.num_genes = None
        self.population_size = None
        self.population = 0
        self.current_generation = 0

    def run(self):
        # Deverá implemetar o método para iterar por todas as gerações
        pass

    def get_best_solution(self):
        # Deverá implementar o método para retornar a melhor solução
        # Default: 0 accuracy, 2000 cooldown, 0 fitness score
        return [0,2000], 0

    # Método para retornar a geração atual
    def get_current_generation(self):
        return self.current_generation
