from decimal import Decimal, ROUND_CEILING

class FinancialEngine:
    def __init__(self, saldo_inicial=1000.0):
        self.saldo = Decimal(str(saldo_inicial))
        self.total_apostado = Decimal('0.00')
        self.lucro_liquido = Decimal('0.00')

    def apostar(self, valor):
        v = Decimal(str(valor))
        if v > self.saldo:
            raise ValueError("Saldo insuficiente para a aposta.")
        self.saldo -= v
        self.total_apostado += v
        return v

    def creditar(self, valor_retorno):
        r = Decimal(str(valor_retorno))
        self.saldo += r
        self.lucro_liquido = self.saldo - Decimal('1000.00')

class BrancoRecoveryProgression:
    def __init__(self, aposta_inicial=1.0, multiplicador_alvo=13):
        self.aposta_inicial = Decimal(str(aposta_inicial))
        self.alvo = self.aposta_inicial * Decimal(str(multiplicador_alvo))
        self.perdas_acumuladas = Decimal('0.00')
        self.nivel = 1

    def proxima_aposta(self):
        if self.nivel == 1:
            return self.aposta_inicial
        calc = (self.alvo + self.perdas_acumuladas) / Decimal('13')
        return calc.quantize(Decimal('0.01'), rounding=ROUND_CEILING)

    def registrar_perda(self, valor_apostado):
        self.perdas_acumuladas += Decimal(str(valor_apostado))
        self.nivel += 1

    def registrar_vitoria(self):
        self.perdas_acumuladas = Decimal('0.00')
        self.nivel = 1

class MartingaleProgression:
    def __init__(self, niveis=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512]):
        self.niveis = [Decimal(str(n)) for n in niveis]
        self.indice = 0

    def proxima_aposta(self):
        return self.niveis[self.indice]

    def registrar_perda(self):
        if self.indice < len(self.niveis) - 1:
            self.indice += 1

    def registrar_vitoria(self):
        self.indice = 0
