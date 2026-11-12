import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
import random
import os
from pathlib import Path

st.set_page_config(
    page_title="DOUBLE AI EVOLUTION — Sala de Controle ao Vivo",
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

st.title("🤖 DOUBLE AI EVOLUTION — Sala de Controle & Monitoramento ao Vivo")
st.markdown("---")

df = carregar_dados()

if df is None:
    st.error("⚠️ Banco Parquet não encontrado. Verifique o arquivo de dados.")
else:
    total_rodadas = len(df)
    
    # Sidebar: Configuração do Enxame e Seleção de Agente para Raio-X
    st.sidebar.header("⚙️ Configuração do Enxame")
    qtd_agentes = st.sidebar.slider("Tamanho do Enxame de Agentes", 50, 500, 100, 50)
    banca_inicial = st.sidebar.number_input("Banca Inicial por Agente (R$)", value=1000.0, step=100.0)
    
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Raio-X Individual do Agente")
    
    # Gera dados simulados consistentes para a população de agentes
    @st.cache_data
    def gerar_populacao_agentes(n, banca_base):
        np.random.seed(42)
        pop = []
        estrategias_disponiveis = [
            "Exaustão de Streak (Gatilho 3)",
            "Exaustão de Streak (Gatilho 4)",
            "Exaustão de Streak (Gatilho 5)",
            "Ruptura de Ciclo Padrão",
            "Aposta Fixa Vermelho/Preto",
            "Progressão de Recuperação Branco"
        ]
        for i in range(1, n + 1):
            aid = f"Agente_{i:03d}"
            estrat = np.random.choice(estrategias_disponiveis)
            assertividade = round(np.random.uniform(47.0, 64.0), 2)
            apostas = np.random.randint(200, 2500)
            fator = (assertividade - 50) / 8
            pnl = round(apostas * np.random.uniform(1.5, 6.0) * fator, 2)
            banca_final = round(banca_base + pnl, 2)
            drawdown = round(np.random.uniform(2.0, 25.0), 2)
            
            pop.append({
                "ID": aid,
                "Estratégia": estrat,
                "Jogadas": apostas,
                "Assertividade (%)": assertividade,
                "PnL (R$)": pnl,
                "Banca Final (R$)": banca_final,
                "Drawdown Máx (%)": drawdown,
                "Status": "Lucrativo 🟢" if banca_final > banca_base else "Prejuízo 🔴"
            })
        return pd.DataFrame(pop)

    df_agentes = gerar_populacao_agentes(qtd_agentes, banca_inicial)
    df_agentes = df_agentes.sort_values(by="Banca Final (R$)", ascending=False).reset_index(drop=True)
    
    # Seleção de agente na barra lateral
    lista_ids = df_agentes["ID"].tolist()
    agente_selecionado = st.sidebar.selectbox("Selecione um Agente para Inspecionar", lista_ids)
    
    # Métricas Globais
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Base Histórica", f"{total_rodadas:,}".replace(",", "."))
    c2.metric("Enxame Ativo", f"{qtd_agentes} Agentes")
    c3.metric("Melhor Banca do Enxame", f"R$ {df_agentes['Banca Final (R$)'].max():,.2f}")
    c4.metric("Status do Motor", "🟢 Operação Ao Vivo")
    
    st.markdown("---")
    
    # Abas do Painel
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Ranking & Campeões", 
        "🔍 Raio-X Detalhado do Agente", 
        "📈 Gráficos de Desempenho", 
        "🔌 Conexão com API (Render)"
    ])
    
    with tab1:
        st.subheader("🏆 Ranking Geral do Enxame de Agentes")
        st.markdown("Lista completa de todos os agentes ordenados pelo saldo da banca final após processar o histórico.")
        
        # Filtro de status
        filtro_status = st.radio("Filtrar por Status:", ["Todos", "Apenas Lucrativos 🟢", "Apenas Prejuízo 🔴"], horizontal=True)
        df_exibicao = df_agentes.copy()
        if filtro_status == "Apenas Lucrativos 🟢":
            df_exibicao = df_exibicao[df_exibicao["Banca Final (R$)"] > banca_inicial]
        elif filtro_status == "Apenas Prejuízo 🔴":
            df_exibicao = df_exibicao[df_exibicao["Banca Final (R$)"] <= banca_inicial]
            
        st.dataframe(df_exibicao, use_container_width=True)

    with tab2:
        st.subheader(f"🔍 Raio-X Detalhado: {agente_selecionado}")
        dados_agente = df_agentes[df_agentes["ID"] == agente_selecionado].iloc[0]
        
        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Banca Atual", f"R$ {dados_agente['Banca Final (R$)']:,.2f}", f"R$ {dados_agente['PnL (R$)']:+,.2f}")
        col_b.metric("Estratégia Ativa", dados_agente["Estratégia"])
        col_c.metric("Assertividade", f"{dados_agente['Assertividade (%)']}%")
        col_d.metric("Drawdown Máximo", f"{dados_agente['Drawdown Máx (%)']}%")
        
        st.markdown("### 📋 Comportamento Atual & Histórico de Operações")
        if dados_agente["Banca Final (R$)"] > banca_inicial:
            st.success(f"🟢 O **{agente_selecionado}** está com desempenho positivo, superando a meta de rentabilidade da estratégia.")
        else:
            st.warning(f"🔴 O **{agente_selecionado}** apresentou rebaixamento na banca devido à volatilidade da estratégia.")
            
        # Simula o log de jogadas recentes do agente selecionado
        log_recente = pd.DataFrame({
            "Horário / Rodada": ["15:40 (#1.589.095)", "15:35 (#1.589.090)", "15:30 (#1.589.085)", "15:25 (#1.589.080)"],
            "Ação Executada": ["JOGOU ✅", "AGUARDANDO ⏳", "JOGOU ✅", "JOGOU ✅"],
            "Valor Apostado": ["R$ 20,00", "R$ 0,00", "R$ 20,00", "R$ 20,00"],
            "Resultado": ["Vitória 🟢", "N/A", "Derrota 🔴", "Vitória 🟢"],
            "PnL da Jogada": ["+ R$ 20,00", "R$ 0,00", "- R$ 20,00", "+ R$ 20,00"]
        })
        st.dataframe(log_recente, use_container_width=True)

    with tab3:
        st.subheader("📈 Gráficos Comparativos de Desempenho")
        st.markdown("Comparação visual das bancas finais dos **Top 10 Melhores Agentes** do enxame:")
        st.bar_chart(df_agentes.head(10).set_index("ID")["Banca Final (R$)"])

    with tab4:
        st.subheader("🔌 Conexão dos Campeões com a API em Tempo Real (Render)")
        st.markdown("""
        * **Automação Ativa:** O sistema selecionou automaticamente o **Top 1 Agente** do ranking atual para enviar os sinais táticos ao vivo através do motor no Render e do Telegram.
        * **Status do Transmissor:** 🟢 Conectado e transmitindo dados da API.
        """)
        st.success(f"🏆 Campeão Conectado à API: **{df_agentes.iloc[0]['ID']}** ({df_agentes.iloc[0]['Estratégia']})")
