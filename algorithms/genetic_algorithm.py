import settings
import random

class GeneticAlgorithm:
    def __init__(self, tower_type):
        self.num_generations = 5
        self.num_genes = 4  # accuracy, cooldown, range, firepower
        self.population_size = 10
        self.tower_type = tower_type
        self.population = self.initialize_population()
        self.current_generation = 0

    def initialize_population(self):
        # Coloca os limites estipulados no settings.py para as torres
        range_min, range_max = settings.TOWER_TYPES[self.tower_type]['range'] # range_min = 50 unidades, range_max = 100 unidades
        cooldown_min, cooldown_max = settings.TOWER_TYPES[self.tower_type]['cooldown'] # cooldown_min = 100 ms, cooldown_max = 4000 ms
        damage_min, damage_max = settings.TOWER_TYPES[self.tower_type]['damage'] # damage_min = 1, damage_max = 3
        # A accuracy não está estipulada no settings.py, mas é um valor entre 0.01 e 1
        
        first_population = [] # Inicializa a lista da primeira "população"
        
        for _ in range(self.population_size): # Aqui inicializa-se a população com valores aleatórios dentro dos limites estipulados, sendo o máximo 10
            individual = [
                random.uniform(0.01, 1), # accuracy
                random.randint(cooldown_min, cooldown_max), # cooldown
                random.randint(range_min, range_max), # range
                random.randint(damage_min, damage_max) # damage
            ]
            first_population.append(individual) # Adiciona o indivíduo à população
        
        return first_population # Retorna a população criada

    def fitness_function(self, individual):
        """
        Como os genes têm valores diferentes, é necessário normalizá-los para o intervalo [0, 1] com base nos limites do settings.py
        Damos também pesos diferentes a cada gene para o fitness score
        """
        # Retira os genes do indivíduo
        accuracy, cooldown, _range, damage = individual

        # Normaliza os valores para o intervalo [0, 1] com base nos limites do settings.py
        n_accuracy = (accuracy - 0.01) / (1.0 - 0.01)  # Intervalo [0.01, 1.0]
        n_cooldown = (4000 - cooldown) / (4000 - 100)   # Inverso de [100, 4000]
        n_range = (_range - 50) / (100 - 50)           # Intervalo [50, 100]
        n_damage = (damage - 1) / (3 - 1)              # Intervalo [1, 3]

        # Peso para cada gene no fitness
        w_accuracy = 0.3
        w_cooldown = 0.5
        w_range = 0.1
        w_damage = 0.1

        # Calcula o fitness score
        score = (
            (n_accuracy * w_accuracy) +
            (n_cooldown * w_cooldown) +
            (n_range * w_range) +
            (n_damage * w_damage)
        )

        # Garante que o fitness score está no intervalo [0, 1]
        return round(max(0, min(1, score)), 3)

    def run_generation(self):
        """
        Corre e melhora uma geração.
        Seleciona os pais, faz o crossover multiponto e por fim faz mutação para criar uma nova população.
        """
        # Inicializa a lista da nova população
        new_pop = []

        # Loop até a nova população ter o mesmo tamanho que a população atual
        while len(new_pop) < self.population_size:
            # Seleciona dois pais
            p1, p2 = self.select()
            # Faz o crossover entre os pais e cria um filho
            c = self.crossover(p1, p2)
            # Faz a mutação do filho
            mutated_c = self.mutate(c)
            # Adiciona o filho alterado à nova população
            new_pop.append(mutated_c)

        # Atualiza a população atual com a nova população
        self.population = new_pop
        self.current_generation += 1

    # Achei necessário adicionar este método para a seleção dos pais, pois não estava a perceber onde o fazer incialmente
    def select(self):
        """
        Faz a seleceção de dois pais com base no fitness score.
        Faz a seleção através de um ranking, onde a probabilidade de ser escolhido aumenta com o fitness score do mesmo.
        """
        # Ordena a população por fitness score
        sorted_pop = sorted(self.population, key=self.fitness_function, reverse=True)
        # Calcula as probabilidades de seleção com base no ranking
        total_rank = sum(range(1, len(sorted_pop) + 1))
        prob = [rank / total_rank for rank in range(len(sorted_pop), 0, -1)]
        
        # Seleciona dois pais com base nas probabilidades
        p1 = random.choices(sorted_pop, weights=prob, k=1)[0]
        p2 = random.choices(sorted_pop, weights=prob, k=1)[0]
        
        return p1, p2

    def crossover(self, parent1, parent2):
        """
        Crossover multiponto entre dois pais.
        Alterna entre os genes dos pais em vários pontos de cruzamento.
        """
        # Determina o número de pontos de cruzamento (pelo menos 1 e no máximo num_genes - 1)
        num_cross_p = random.randint(1, 2)
        
        # Cria aleatoriamente os pontos de cruzamento
        cross_p = sorted(random.sample(range(1, self.num_genes), num_cross_p))
        
        # Alterna entre os pais para criar o filho
        c = []
        p = False  # Serve para alternar entre os pais
        last_point = 0
        
        for point in cross_p:
            # Adiciona genes do pai atual até o ponto de cruzamento
            if p:
                c.extend(parent1[last_point:point])
            else:
                c.extend(parent2[last_point:point])
            
            # Alterna o pai e atualiza o último ponto de cruzamento
            p = not p
            last_point = point
        
        # Adiciona os genes restantes do último ponto até o final
        if p:
            c.extend(parent1[last_point:])
        else:
            c.extend(parent2[last_point:])
        
        return c

    def mutate(self, individual):
        """
        Mutação aleatória uniforme de genes do indivíduo.
        Em vez de mudar todos os genes, apenas muda um gene com uma probabilidade de 0.1 (10%).
        """
        # Loop através de cada gene do indivíduo
        for i in range(len(individual)):
            # Muda o gene se a probabilidade for menor que 0.1 (o random.random() gera um número entre 0 e 1)
            if random.random() < 0.1:
                # Usei como base os limites usados anteriormente para a inicialização da população
                if i == 0:  # accuracy
                    individual[i] = round(random.uniform(0.01, 1.0), 3)
                elif i == 1:  # cooldown
                    cooldown_min, cooldown_max = settings.TOWER_TYPES[self.tower_type]['cooldown']
                    individual[i] = random.randint(cooldown_min, cooldown_max)
                elif i == 2:  # range
                    range_min, range_max = settings.TOWER_TYPES[self.tower_type]['range']
                    individual[i] = random.randint(range_min, range_max)
                elif i == 3:  # firepower
                    damage_min, damage_max = settings.TOWER_TYPES[self.tower_type]['damage']
                    individual[i] = random.randint(damage_min, damage_max)
        
        return individual

    def get_best_solution(self, num_solutions=1):
        """
        Retorna as melhores soluções e seus fitness scores.
        Pelo que percebi o argumento num_solutions é o número de soluções que queremos e é utilizado na classe game.py.
        """
        # Calcula o fitness score de cada indivíduo
        fitness_scores = [(self.fitness_function(i), i) for i in self.population]
        # Ordena os indivíduos pelo fitness score
        fitness_scores.sort(reverse=True, key=lambda x: x[0])
        # Retorna as melhores soluções e seus os fitness scores (até ao num_solutions)
        best_solutions = [i for _, i in fitness_scores[:num_solutions]]
        best_fitness_scores = [s for s, _ in fitness_scores[:num_solutions]]

        return best_solutions, best_fitness_scores

    def get_current_generation(self):
        """
        Retorna um número inteiro que representa a geração atual.
        """
        return self.current_generation

    def run(self):
        """
        Corre o algoritmo genético até que o fitness score médio seja maior ou igual a 0.95 
        ou até que o número máximo de gerações seja atingido.
        """
        max_gen = 25  # Define o limite de gerações

        # Loop até que as gerações atinjam o limite
        while self.current_generation < max_gen:
            # Corre uma geração
            self.run_generation()
            # Obtém as melhores 6 soluções e os seus fitness scores
            top_s, top_f = self.get_best_solution(6)
            # Calcula o fitness score médio das melhores soluções
            avg_fitness = round(sum(top_f) / len(top_f), 3)
            # Imprime o fitness score médio
            print(f"Generation {self.current_generation} -> Average of {avg_fitness}")
            # Verifica se o fitness score médio é maior ou igual a 0.95
            if avg_fitness >= 0.95:
                break

        # Verifica se o número máximo de gerações foi atingido
        if self.current_generation >= max_gen:
            print(f"Maximum number of generations reached ({max_gen}).")
