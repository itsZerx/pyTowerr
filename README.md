## pyTowerr - A Python Tower Defence 2D Game
#### Applications: Genetic Algorithms &amp; Reinforcement Learning
*Autor: António Raimundo*

Código-base para a Unidade Curricular (UC)
de Inteligência Artificial do Iscte-Sintra.

### Download do projeto
Para poderem fazer o _download_ do projeto, deverão seguir as instruções presentes na documentação do código-base. 
Após garantirem que o código-base já se encontra nas vossas máquinas, procedam para o
próximo passo.

### Configuração inicial
Têm de garantir que possuem os seguintes requisitos para poderem importar corretamente
o projeto-base para o vosso IDE (Visual Studio Code / PyCharm):
1. Ter a versão Python 3.10 ou superior instalada nas vossas máquinas.
2. Criar um ambiente virtual específico para este projeto. Para tal,
executem algumas operações:
   1. Atualizem a versão do Python Package Manager (pip): ``pip install --upgrade pip``;
   2. Criação do ambiente virtual (**recomendado**): ``conda create -n NOME_ESCOLHIDO python=3.11``;
   3. Configurar interpretador no VS Code ou PyCharm (se fizeram todos os passos corretamente, deverá aparecer nos vossos IDEs o novo ambiente virtual que criaram).

Após terminarem a configuração inicial, prossigam para mais uns comandos adicionais:

### Comandos iniciais:
Para garantir que o projeto base inicia sem problemas, devem importar o projeto, e no terminal 
(garantir que estão localizados na **pasta principal - pyTowerr**)
executem o seguinte comando:

``pip install -r requirements.txt``

### Ficheiro original `genetic_algorithm.py`:
Se houver necessidade de terem acesso ao código original do ficheiro `algorithms/genetic_algorithm.py`, têm abaixo a configuração base:
```python
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
```