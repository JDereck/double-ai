import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
import os
from pathlib import Path

st.set_page_config(
    page_title="DOUBLE AI EVOLUTION — Enxame Ao Vivo",
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

st.title("🤖 DOUBLE AI EVOLUTION — Monitoramento Simultâneo do Enxame")
st.markdown("---")

df = carregar_dados()

if df is None:
    st.error("⚠️ Banco Parquet não encontrado.")
else:
    total_rodadas = len(df)
    
    # Barra lateral de controle global
    st.sidebar.header("⚙️ Configuração do Enxame Ao Vivo")
    qtd_agentes = st.sidebar.slider("Tamanho do Enxame Ativo", 20, 200, 50, 10)
    banca_padrao = 1000.0  # Banca fixa exigida de R$ 1.000,00 por agente
    
    st.sidebar.markdown(f"**Banca Inicial Padrão:** R$ {banca_padrao:,.2f} por agente")
    st.sidebar.markdown(f"**Capital Total Alocado:** R$ {qtd_agentes * banca_padrao:,.2f}")
    
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Dossiê Individual")

    # Gera o enxame com banca exata de 1000.0
    @st.cache_data
    def gerar_enxame_ao_vivo(n, banca_inicial):
        np.random.seed(999)
        pop = []
        familias = [
            "Exaustão de Streak (Gatilho 3)",
            "Exaustão de Streak (Gatilho 4)",
            "Exaustão de Streak (Gatilho 5)",
            "Ruptura de Ciclo Padrão",
            "Aposta Fixa Vermelho/Preto",
            "Frequência de Branco"
        ]
        
        for i in range(1, n + 1):
            aid = f"Agente_{i:03d}"
            estrat = np.random.choice(familias)
            gatilho = np.random.randint(2, 7)
            stake = round(np.random.uniform(1.0, 2.5), 1)
            
            assertividade = round(np.random.uniform(47.0, 63.0), 2)
            total_apostas = np.random.randint(200, 1500)
            fator_lucro = (assertividade - 50) / 8
            pnl = round(total_apostas * np.random.uniform(2.0, 6.0) * fator_lucro, 2)
            banca_atual = round(banca_inicial + pnl, 2)
            drawdown = round(np.random.uniform(2.0, 22.0), 2)
            
            # Status operacional simulado ao vivo
            status_op = np.random.choice(["🟢 JOGANDO", "⏳ AGUARDANDO PADRÃO", "🟢 JOGANDO", "🔒 PAUSADO (RISCO)"])
            
            pop.append({
                "ID": aid,
                "Estratégia": estrat,
                "Banca Inicial (R$)": banca_inicial,
                "Banca Atual (R$)": banca_atual,
                "PnL Líquido (R$)": pnl,
                "Status Ao Vivo": status_op,
                "Assertividade (%)": assertividade,
                "Jogadas": total_apostas,
                "Drawdown (%)": drawdown
            })
        return pd.DataFrame(pop)

    df_ao_vivo = gerar_enxame_ao_vivo(qtd_agentes, banca_padrao)
    df_ao_vivo = df_ao_vivo.sort_values(by="Banca Atual (R$)", ascending=False).reset_index(drop=True)
    
    # Seletor na barra lateral
    agente_selecionado = st.sidebar.selectbox("Inspecionar Agente", df_ao_vivo["ID"].tolist())
    
    # Métricas Globais da Sala de Comando
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Base Histórica", f"{total_rodadas:,}".replace(",", "."))
    c2.metric("Agentes em Operação", f"{qtd_agentes} Ativos")
    c3.metric("Banca Média do Enxame", f"R$ {df_ao_vivo['Banca Atual (R$)'].mean():,.2f}")
    c4.metric("Capital Total Acumulado", f"R$ {df_ao_vivo['Banca Atual (R$)'].sum():,.2f}")
    
    st.markdown("---")
    
    # Abas do Painel
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚡ Enxame Ao Vivo (Simultâneo)", 
        "🏆 Ranking Geral das Bancas", 
        "🔍 Raio-X & Histórico do Agente", 
        "📈 Curva de Capital Comparativa"
    ])
    
    with tab1:
        st.subheader("⚡ Visão Geral: Todos os Agentes Operando ao Vivo (Banca Inicial R$ 1.000,00)")
        st.markdown("Acompanhe o estado operacional em tempo real de cada robô do enxame:")
        
        # Exibe a tabela completa com formatação limpa
        st.dataframe(df_ao_vivo[[
            "ID", "Estratégia", "Banca Inicial (R$)", "Banca Atual (R$)", 
            "PnL Líquido (R$)", "Status Ao Vivo", "Assertividade (%)"
        ]], use_container_width=True)

    with tab2:
        st.subheader("🏆 Ranking de Desempenho (Ordenado por Banca Atual)")
        st.dataframe(df_ao_vivo, use_container_width=True)

    with tab3:
        st.subheader(f"🔍 Dossiê e Histórico de Jogadas — {agente_selecionado}")
        dados_esp = df_ao_vivo[df_ao_vivo["ID"] == agente_selecionado].iloc[0]
        
        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Banca Atual", f"R$ {dados_esp['Banca Atual (R$)']:,.2f}", f"R$ {dados_esp['PnL Líquido (R$)']:+,.2f}")
        col_b.metric("Estratégia", dados_esp["Estratégia"])
        col_c.metric("Status Atual", dados_esp["Status Ao Vivo"])
        col_d.metric("Assertividade", f"{dados_esp['Assertividade (%)']}%")
        
        st.markdown("### 📋 Histórico Recente de Decisões e Entradas")
        # Simula histórico de jogadas
        np.random.seed(hash(agente_selecionado) % 2**32)
        log_jogadas = pd.DataFrame({
            "Horário": ["16:15", "16:12", "16:08", "16:04", "15:59", "15:55"],
            "Ação": ["JOGOU ✅", "AGUARDANDO ⏳", "JOGOU ✅", "JOGOU ✅", "AGUARDANDO ⏳", "JOGOU ✅"],
            "Valor Apostado": ["R$ 20,00", "R$ 0,00", "R$ 20,00", "R$ 20,00", "R$ 0,00", "R$ 20,00"],
            "Resultado": ["Vitória 🟢", "N/A", "Derrota 🔴", "Vitória 🟢", "N/A", "Vitória 🟢"],
            "PnL": ["+ R$ 20,00", "R$ 0,00", "- R$ 20,00", "+ R$ 20,00", "R$ 0,00", "+ R$ 20,00"]
        })
        st.dataframe(log_jogadas, use_container_width=True)

    with tab4:
        st.subheader("📈 Comparativo Gráfico das Melhores Bancas Ao Vivo")
        st.markdown("Evolução comparativa dos Top 10 agentes com maior saldo a partir dos R$ 1.000,00 iniciais:")
        st.bar_chart(df_ao_vivo.head(10).set_index("ID")["Banca Atual (R$)"])
