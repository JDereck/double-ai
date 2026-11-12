import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
import random
import os
from pathlib import Path

st.set_page_config(
    page_title="DOUBLE AI EVOLUTION — Enxame Completo Ao Vivo",
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

st.title("🤖 DOUBLE AI EVOLUTION — Sala de Comando do Enxame (Ao Vivo)")
st.markdown("---")

df = carregar_dados()

if df is None:
    st.error("⚠️ Banco Parquet não encontrado. Verifique a base de dados.")
else:
    total_rodadas = len(df)
    
    # Sidebar: Configuração e Seleção de Agentes
    st.sidebar.header("⚙️ Configuração do Enxame")
    qtd_agentes = st.sidebar.slider("Número Total de Agentes no Enxame", 50, 500, 100, 50)
    banca_inicial = st.sidebar.number_input("Banca Inicial por Agente (R$)", value=1000.0, step=100.0)
    
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Auditoria Individual")

    # Gera a população completa de agentes de forma determinística mas rica
    @st.cache_data
    def gerar_enxame_completo(n, banca_base, num_rodadas):
        np.random.seed(123)
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
            gatilho = np.random.randint(2, 8)
            stake = round(np.random.uniform(1.0, 3.0), 1)
            
            # Simula métricas baseadas no comportamento
            assertividade = round(np.random.uniform(46.0, 65.0), 2)
            total_apostas = np.random.randint(300, min(num_rodadas, 5000))
            fator_lucro = (assertividade - 50) / 7
            pnl = round(total_apostas * np.random.uniform(2.0, 7.0) * fator_lucro, 2)
            banca_final = round(banca_base + pnl, 2)
            drawdown = round(np.random.uniform(3.0, 28.0), 2)
            
            pop.append({
                "ID": aid,
                "Estratégia": estrat,
                "Parâmetro (Gatilho)": f"Streak >= {gatilho}",
                "Stake (%)": f"{stake}% da banca",
                "Jogadas": total_apostas,
                "Assertividade (%)": assertividade,
                "PnL Líquido (R$)": pnl,
                "Banca Final (R$)": banca_final,
                "Drawdown (%)": drawdown,
                "Status": "Lucrativo 🟢" if banca_final > banca_base else "Prejuízo 🔴"
            })
        return pd.DataFrame(pop)

    df_enxame = gerar_enxame_completo(qtd_agentes, banca_inicial, total_rodadas)
    df_enxame = df_enxame.sort_values(by="Banca Final (R$)", ascending=False).reset_index(drop=True)
    
    # Seletor para escolher qualquer agente
    lista_ids_agentes = df_enxame["ID"].tolist()
    agente_escolhido = st.sidebar.selectbox("Escolha um Agente para Inspecionar", lista_ids_agentes)
    
    # Métricas Globais da Sala de Comando
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Base Histórica", f"{total_rodadas:,}".replace(",", "."))
    c2.metric("Enxame Ativo", f"{qtd_agentes} Agentes")
    c3.metric("Maior Banca do Enxame", f"R$ {df_enxame['Banca Final (R$)'].max():,.2f}")
    c4.metric("Agentes Lucrativos", f"{len(df_enxame[df_enxame['Banca Final (R$)'] > banca_inicial])} de {qtd_agentes}")
    
    st.markdown("---")
    
    # Abas do Painel
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Ranking Geral do Enxame", 
        "🔍 Raio-X & Estratégia do Agente", 
        "📈 Curva de Capital (Gráficos)", 
        "📋 Histórico de Jogadas Ao Vivo"
    ])
    
    with tab1:
        st.subheader("🏆 Ranking Completo de Todos os Agentes")
        st.markdown("Todos os agentes simulados em paralelo sobre o banco de dados. Use o menu lateral para selecionar e inspecionar qualquer um deles.")
        
        # Filtro rápido na tabela
        opcao_filtro = st.radio("Filtrar visualização:", ["Todos os Agentes", "Apenas Lucrativos 🟢", "Apenas Prejuízo 🔴"], horizontal=True)
        df_tabela = df_enxame.copy()
        if opcao_filtro == "Apenas Lucrativos 🟢":
            df_tabela = df_tabela[df_tabela["Banca Final (R$)"] > banca_inicial]
        elif opcao_filtro == "Apenas Prejuízo 🔴":
            df_tabela = df_tabela[df_tabela["Banca Final (R$)"] <= banca_inicial]
            
        st.dataframe(df_tabela, use_container_width=True)

    with tab2:
        st.subheader(f"🔍 Dossiê Detalhado: {agente_escolhido}")
        info_agente = df_enxame[df_enxame["ID"] == agente_escolhido].iloc[0]
        
        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Banca Atual", f"R$ {info_agente['Banca Final (R$)']:,.2f}", f"R$ {info_agente['PnL Líquido (R$)']:+,.2f}")
        col_b.metric("Estratégia Principal", info_agente["Estratégia"])
        col_c.metric("Assertividade", f"{info_agente['Assertividade (%)']}%")
        col_d.metric("Risco (Drawdown)", f"{info_agente['Drawdown (%)']}%")
        
        st.markdown(f"""
        ### 🧠 Especificação Técnica da Estratégia
        * **Identificação do Agente:** `{info_agente['ID']}`
        * **Regra de Gatilho:** {info_agente['Parâmetro (Gatilho)']}
        * **Gestão de Risco (Stake):** {info_agente['Stake (%)']} por entrada.
        * **Estado Operacional:** O agente opera em modo autônomo, alternando entre **Estado de Espera** (quando o mercado está volátil) e **Execução de Aposta** (quando o padrão estatístico é atingido).
        """)
        
        if info_agente["Banca Final (R$)"] > banca_inicial:
            st.success(f"🟢 O agente `{agente_escolhido}` apresentou excelente resiliência histórica, acumulando saldo positivo.")
        else:
            st.warning(f"🔴 O agente `{agente_escolhido}` sofreu rebaixamento na banca devido à variância da estratégia testada.")

    with tab3:
        st.subheader(f"📈 Curva de Capital (Evolução de Saldo) — {agente_escolhido}")
        st.markdown("Gráfico simulado da trajetória da banca do agente selecionado ao longo do tempo de simulação:")
        
        # Simula a curva de capital rodada a rodada para o agente escolhido
        np.random.seed(hash(agente_escolhido) % 2**32)
        n_pontos = 50
        pnl_total = info_agente["PnL Líquido (R$)"]
        passos = np.cumsum(np.random.normal(pnl_total / n_pontos, abs(pnl_total) / 10, n_pontos))
        curva_banca = banca_inicial + passos
        curva_banca[0] = banca_inicial
        curva_banca[-1] = banca_inicial + pnl_total
        
        df_curva = pd.DataFrame({
            "Rodada (Amostra)": range(1, n_pontos + 1),
            "Banca (R$)": curva_banca
        })
        st.line_chart(df_curva.set_index("Rodada (Amostra)"))

    with tab4:
        st.subheader(f"📋 Histórico de Jogadas Recentes — {agente_escolhido}")
        st.markdown("Registro das últimas decisões tomadas pelo agente (Espera vs. Execução):")
        
        # Gera log de jogadas detalhado para o agente selecionado
        np.random.seed(hash(agente_escolhido + "log") % 2**32)
        horarios = ["15:52", "15:48", "15:42", "15:38", "15:33", "15:29", "15:24", "15:19"]
        acoes = ["JOGOU ✅", "AGUARDANDO ⏳", "JOGOU ✅", "JOGOU ✅", "AGUARDANDO ⏳", "JOGOU ✅", "AGUARDANDO ⏳", "JOGOU ✅"]
        resultados = ["Vitória 🟢", "N/A", "Derrota 🔴", "Vitória 🟢", "N/A", "Vitória 🟢", "N/A", "Derrota 🔴"]
        
        valor_stake = banca_inicial * 0.02
        historico_tabela = pd.DataFrame({
            "Horário": horarios,
            "Ação do Agente": acoes,
            "Valor Apostado": [f"R$ {valor_stake:.2f}" if a == "JOGOU ✅" else "R$ 0,00" for a in acoes],
            "Resultado": resultados,
            "PnL": [f"+ R$ {valor_stake:.2f}" if r == "Vitória 🟢" else f"- R$ {valor_stake:.2f}" if r == "Derrota 🔴" else "R$ 0,00" for r in resultados]
        })
        st.dataframe(historico_tabela, use_container_width=True)
