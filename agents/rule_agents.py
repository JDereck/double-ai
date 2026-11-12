from decimal import Decimal
from engine.financial_engine import FinancialEngine

class BaseAgent:
    def __init__(self, agent_id, name, strategy_family, saldo_inicial=1000.0):
        self.agent_id = agent_id
        self.name = name
        self.strategy_family = strategy_family
        self.fe = FinancialEngine(saldo_inicial)
        self.ativo = True
        self.historico_apostas = []
        self.entradas_total = 0
        self.acertos_total = 0

    def decidir(self, historico_passado):
        """ Retorna (modalidade, valor_aposta) ou (None, 0) se decidir esperar """
        raise NotImplementedError

    def registrar_resultado(self, rodada_atual, ganhou, valor_pago):
        if ganhou:
            self.fe.creditar(valor_pago)
            self.acertos_total += 1
        self.entradas_total += 1
        if self.fe.saldo <= Decimal('0.10'):
            self.ativo = False

class FixedBetAgent(BaseAgent):
    """ Agente de aposta fixa em uma cor específica """
    def __init__(self, agent_id, name, cor_alvo, valor_aposta=1.0):
        super().__init__(agent_id, name, "Aposta Fixa")
        self.cor_alvo = cor_alvo # 0=Branco, 1=Vermelho, 2=Preto
        self.valor = Decimal(str(valor_aposta))

    def decidir(self, historico_passado):
        if not self.ativo or self.fe.saldo < self.valor:
            return None, Decimal('0.00')
        return self.cor_alvo, self.valor
