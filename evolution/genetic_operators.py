import random
from decimal import Decimal
from agents.rule_agents import FixedBetAgent

class GeneticEngine:
    def __init__(self, population_size=500):
        self.population_size = population_size
        self.generation = 1

    def criar_populacao_inicial(self):
        populacao = []
        for i in range(1, self.population_size + 1):
            cor = i % 3  # 0=Branco, 1=Vermelho, 2=Preto
            valor = 1.0
            ag = FixedBetAgent(i, f"Agente_Gen1_{i}", cor_alvo=cor, valor_aposta=valor)
            ag.geracao = 1
            populacao.append(ag)
        return populacao

    def evoluir_geracao(self, populacao_atual):
        # Avalia e seleciona os melhores com base no saldo final (aptidão / fitness)
        populacao_ordenada = sorted(populacao_atual, key=lambda x: float(x.fe.saldo), reverse=True)
        
        # Preserva os top 20% (Elite)
        corte = int(self.population_size * 0.2)
        elite = populacao_ordenada[:corte]
        
        nova_populacao = list(elite)
        self.generation += 1

        # Preenche o restante gerando descendentes mutados da elite
        id_counter = self.population_size + 1
        while len(nova_populacao) < self.population_size:
            pai = random.choice(elite)
            filho_cor = pai.cor_alvo
            if random.random() < 0.2:  # 20% de chance de mutação na cor alvo
                filho_cor = random.choice([0, 1, 2])
            
            filho = FixedBetAgent(id_counter, f"Agente_Gen{self.generation}_{id_counter}", cor_alvo=filho_cor, valor_aposta=float(pai.valor))
            filho.geracao = self.generation
            nova_populacao.append(filho)
            id_counter += 1

        return nova_populacao
