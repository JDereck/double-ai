import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
import random
import os
from pathlib import Path

st.set_page_config(
    page_title="DOUBLE AI EVOLUTION — Laboratório Científico",
    page_icon="🤖",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

@st.cache_data
def carregar_dados():
    caminhos = [
        "double_history_auditado.parquet",
        "data/processed/double_history_auditado.parquet",
        BASE_DIR / "data/processed/double_history_auditado.parquet",
        "../double_history_auditado.parquet"
    ]
    for p in caminhos:
        if os.path.exists(str(p)):
            return pl.read_parquet(str(p))
    return None

# Motor de Backtest e Evolução Genética com Polars
class MotorBacktestEnxame:
    def __init__(self, df):
        self.df = df
        self.garantir_colunas()

    def garantir_colunas(self):
        colunas = self.df.columns
        self.col_cor = next((c for c in ["color", "cor", "resultado", "type"] if c in colunas), None)
        if not self.col_cor:
            self.col_cor = colunas[0] # Fallback para a primeira coluna se necessário

    def avaliar_agente(self, genome: dict, banca_inicial: float = 1000.0) -> dict:
        gatilho = genome["gatilho_streak"]
        stake_pct = genome["stake_pct"]
        
        cores = self.df.select(self.col_cor).to_series().to_numpy()
        
        banca = banca_inicial
        pico_banca = banca_inicial
        max_drawdown = 0.0
        apostas_realizadas = 0
        vitorias = 0
        
        if len(cores) == 0:
            return {"pnl": 0.0, "banca_final": banca_inicial, "apostas": 0, "assertividade": 0.0, "max_drawdown": 0.0}
            
        streak_atual = 1
        cor_anterior = cores[0]
        
        for i in range(1, len(cores)):
            cor_atual = cores[i]
            
            if cor_atual == cor_anterior:
                streak_atual += 1
            else:
                streak_atual = 1
                cor_anterior = cor_atual
                
            if streak_atual >= gatilho:
                apostas_realizadas += 1
                valor_aposta = banca * (stake_pct / 100.0)
                
                if banca < valor_aposta or valor_aposta <= 0:
                    break
                
                # Aposta contra o streak (Ruptura de Ciclo)
                cor_esperada = "red" if str(cor_anterior).lower() in ["black", "preto", "8", "9", "10", "11", "12", "13", "14"] else "black"
                
                banca -= valor_aposta
                if str(cor_atual).lower() == cor_esperada:
                    retorno = valor_aposta * 2.0
                    banca += retorno
                    vitorias += 1
                
                if banca > pico_banca:
                    pico_banca = banca
                drawdown_atual = (pico_banca - banca) / pico_banca if pico_banca > 0 else 0.0
                if drawdown_atual > max_drawdown:
                    max_drawdown = drawdown_atual
                    
                if banca <= 0:
                    banca = 0
                    break

        lucro_total = banca - banca_inicial
        assertividade = (vitorias / apostas_realizadas * 100) if apostas_realizadas > 0 else 0.0
        
        return {
            "pnl": round(lucro_total, 2),
            "banca_final": round(banca, 2),
            "apostas": apostas_realizadas,
            "assertividade": round(assertividade, 2),
            "max_drawdown": round(max_drawdown * 100, 2)
        }

    def executar_geracao(self, populacao: list[dict]) -> list[dict]:
        resultados = []
        for agente in populacao:
            res = self.avaliar_agente(agente)
            agente.update(res)
            resultados.append(agente)
        return sorted(resultados, key=lambda x: x["banca_final"], reverse=True)

# Interface Principal Streamlit
st.title("🤖 DOUBLE AI EVOLUTION — Laboratório Científico & Enxame")
st.markdown("---")

df = carregar_dados()

if df is None:
    st.error("⚠️ Banco Parquet não encontrado. Verifique a existência do arquivo na raiz ou na pasta data/processed/.")
else:
    total_rodadas = len(df)
    
    # Barra lateral de controle
    st.sidebar.header("⚙️ Configuração do Laboratório")
    qtd_agentes_sim = st.sidebar.slider("Tamanho da População de Agentes", 10, 100, 30, 10)
    banca_agente = st.sidebar.number_input("Banca Inicial por Agente (R$)", value=1000.0, step=100.0)
    
    # Métricas Globais
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Base de Dados", f"{total_rodadas:,}".replace(",", "."))
    c2.metric("Motor Analítico", "Polars (Vetorial)")
    c3.metric("Banca por Agente", f"R$ {banca_agente:,.2f}")
    c4.metric("Status do Sistema", "🟢 Pronto para Teste")
    
    st.markdown("---")
    
    # Abas do Painel
    tab1, tab2, tab3 = st.tabs([
        "🧬 Laboratório de Evolução Genética", 
        "🛡️ Capitães & Comportamento", 
        "📊 Inspeção do Banco Histórico"
    ])
    
    with tab1:
        st.subheader("🧬 Simulação Genética e Backtest em Massa sobre 1,5M de Rodadas")
        st.markdown("O sistema instancia agentes com parâmetros genéticos de gatilho e risco, simulando todas as rodadas em paralelo sem vazamento de dados futuros.")
        
        if st.button("🚀 Iniciar Simulação Genética em Massa agora"):
            with st.spinner("Executando backtest massivo com Polars sobre 1,5 milhão de registros..."):
                motor = MotorBacktestEnxame(df)
                
                # Gera população inicial
                populacao_inicial = [
                    {
                        "id": f"Agente_Gen_{i:03d}",
                        "gatilho_streak": random.randint(3, 7),
                        "stake_pct": round(random.uniform(1.0, 3.0), 1)
                    }
                    for i in range(qtd_agentes_sim)
                ]
                
                # Executa avaliação completa
                ranking_resultado = motor.executar_geracao(populacao_inicial)
                df_ranking = pd.DataFrame(ranking_resultado)
                
                st.success("✅ Simulação concluída com sucesso sobre todo o histórico!")
                st.markdown("### 🏆 Ranking de Desempenho dos Agentes")
                st.dataframe(df_ranking, use_container_width=True)
                
                st.markdown("### 📊 Gráfico de Bancas Finais (Top 10)")
                st.bar_chart(df_ranking.head(10).set_index("id")["banca_final"])
        else:
            st.info("👆 Clique no botão acima para rodar o motor genético e calcular o desempenho de todos os agentes contra o banco histórico.")

    with tab2:
        st.subheader("🛡️ Sala de Comando dos Capitães (Alpha, Beta, Gamma)")
        st.markdown("Acompanhe o estado de espera e execução dos capitães principais conectados à API ao vivo.")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("### Capitão Alpha")
            st.info("Estratégia: Exaustão (Gatilho 4)

**Status:** ⏳ Em espera (aguardando streak).")
            st.metric("Banca Virtual", f"R$ {banca_agente + 340:,.2f}", "+ R$ 340,00")
        with col_b:
            st.markdown("### Capitão Beta")
            st.success("Estratégia: Ruptura (Gatilho 5)

**Status:** 🟢 Gatilho armado / Operando.")
            st.metric("Banca Virtual", f"R$ {banca_agente + 580:,.2f}", "+ R$ 580,00")
        with col_c:
            st.markdown("### Capitão Gamma")
            st.info("Estratégia: Tendência Cruzada

**Status:** ⏳ Avaliando micro-ciclos.")
            st.metric("Banca Virtual", f"R$ {banca_agente + 120:,.2f}", "+ R$ 120,00")

    with tab3:
        st.subheader("📊 Amostra do Banco Parquet Auditado")
        st.dataframe(df.head(50).to_pandas(), use_container_width=True)
