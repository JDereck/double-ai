import polars as pl
from decimal import Decimal

class ChronologicalSimulator:
    def __init__(self, parquet_path):
        self.df = pl.read_parquet(parquet_path)
        self.total_rodadas = len(self.df)

    def rodar_simulacao_piloto(self, agentes, max_rodadas=10000):
        print(f"Iniciando simulação para {len(agentes)} agentes em {max_rodadas:,} rodadas (Zero Leakage)...")
        
        # Converte para dict para acesso ultra-rápido no loop
        timestamps = self.df["timestamp"].head(max_rodadas).to_list()
        rolls = self.df["roll"].head(max_rodadas).to_list()
        colors = self.df["color_id"].head(max_rodadas).to_list()
        quebras = self.df["quebra_sessao"].head(max_rodadas).to_list() if "quebra_sessao" in self.df.columns else [False]*max_rodadas

        for i in range(1, max_rodadas):
            t_atual = timestamps[i]
            roll_atual = rolls[i]
            color_atual = colors[i]
            houve_quebra = quebras[i]

            # Histórico estritamente do passado: índice 0 até i-1
            # (Garante Zero Leakage absoluto)
            passado_recente = colors[:i]

            for agente in agentes:
                if not agente.ativo:
                    continue

                # Se houve quebra de sessão (>5 min offline), agentes com progressão reiniciam o ciclo por segurança
                if houve_quebra and hasattr(agente, "reset_sessao"):
                    agente.reset_sessao()

                modalidade, valor = agente.decidir(passado_recente)
                if modalidade is not None and valor > 0:
                    try:
                        aposta_efetiva = agente.fe.apostar(valor)
                        ganhou = (modalidade == color_atual)
                        
                        # Cálculo do retorno: 14x para branco (0), 2x para vermelho/preto (1, 2)
                        multiplicador = Decimal('14') if modalidade == 0 else Decimal('2')
                        retorno = aposta_efetiva * multiplicador if ganhou else Decimal('0.00')

                        agente.registrar_resultado(color_atual, ganhou, retorno)
                        
                        if hasattr(agente, "atualizar_progressao"):
                            agente.atualizar_progressao(ganhou)

                    except ValueError:
                        # Saldo insuficiente
                        agente.ativo = False

        print("Simulação piloto concluída com sucesso!")
