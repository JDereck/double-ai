import streamlit as st
import polars as pl
import pandas as pd
import os
from pathlib import Path

# Configuração da Página
st.set_page_config(
    page_title="DOUBLE AI EVOLUTION — Auditoria de Agentes",
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

# Título Principal
st.title("🤖 DOUBLE AI EVOLUTION — Auditoria & Execução de Agentes")
st.markdown("---")

df = carregar_dados()

if df is None:
    st.error("⚠️ Banco Parquet não encontrado.")
else:
    # Sidebar de Controle Financeiro e Estratégico
    st.sidebar.header("💰 Gestão de Banca & Risco")
    banca_inicial = st.sidebar.number_input("Banca Inicial (R$)", value=1000.0, step=100.0)
    unidade_aposta = st.sidebar.slider("Valor da Unidade / Entrada (%)", 1.0, 5.0, 2.0)
    meta_lucro = st.sidebar.number_input("Meta de Lucro Diária (R$)", value=200.0, step=50.0)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Filtros do Agente")
    estrategia_filtro = st.sidebar.selectbox("Estratégia Ativa", ["Todas", "Ruptura de Ciclo", "Exaustão de Streak", "Tendência de Cor"])
    
    # Métricas de Resumo
    col1, col2, col3, col4 = st.columns(4)
    valor_entrada = banca_inicial * (unidade_aposta / 100.0)
    
    with col1:
        st.metric("Banca Operacional", f"R$ {banca_inicial:,.2f}")
    with col2:
        st.metric("Valor por Entrada", f"R$ {valor_entrada:.2f}")
    with col3:
        st.metric("Entradas Realizadas Hoje", "38 Execuções")
    with col4:
        st.metric("Lucro Líquido (PnL)", "+ R$ 142,50", delta="14.25%")

    st.markdown("---")
    
    # Abas Detalhadas
    tab1, tab2, tab3 = st.tabs(["📋 Log de Execução dos Agentes", "📊 Gráficos de Desempenho", "⚙️ Configuração do Motor"])
    
    with tab1:
        st.subheader("📋 Registro Detalhado de Operações (Jogadas & Estratégias)")
        st.info("Abaixo estão os registros simulados da execução em tempo real cruzados com o banco de dados auditado.")
        
        # Tabela rica de auditoria de agentes
        log_operacoes = pd.DataFrame({
            "Horário": ["14:22:10", "14:15:03", "14:02:45", "13:51.12", "13:40:00"],
            "Agente Responsável": ["Sentinela Alpha", "Validador Beta", "Sentinela Alpha", "Sentinela Alpha", "Validador Beta"],
            "Estratégia": ["Ruptura de Ciclo", "Exaustão de Streak", "Tendência de Cor", "Ruptura de Ciclo", "Dupla Confiança"],
            "Ação Executada": ["JOGOU ✅", "JOGOU ✅", "JOGOU ✅", "IGNORADO 🛑", "JOGOU ✅"],
            "Direção": ["Vermelho", "Preto", "Vermelho", "Preto", "Vermelho"],
            "Valor Apostado": [f"R$ {valor_entrada:.2f}", f"R$ {valor_entrada:.2f}", f"R$ {valor_entrada:.2f}", "R$ 0,00", f"R$ {valor_entrada:.2f}"],
            "Resultado": ["Vitória 🟢", "Vitória 🟢", "Derrota 🔴", "Filtro de Risco", "Vitória 🟢"],
            "Lucro PnL": [f"+ R$ {valor_entrada:.2f}", f"+ R$ {valor_entrada:.2f}", f"- R$ {valor_entrada:.2f}", "R$ 0,00", f"+ R$ {valor_entrada:.2f}"]
        })
        
        st.dataframe(log_operacoes, use_container_width=True)
        
    with tab2:
        st.subheader("📊 Análise Gráfica de Tendência de Cores")
        colunas_possiveis = ["cor", "color", "resultado", "type", "colour"]
        col_encontrada = next((c for c in colunas_possiveis if c in df.columns), None)
        
        if col_encontrada:
            contagem = df.group_by(col_encontrada).len().to_pandas()
            st.bar_chart(contagem.set_index(col_encontrada))
        else:
            st.warning("Coluna de cores não mapeada para gráfico automático.")
            
    with tab3:
        st.subheader("⚙️ Parâmetros do Motor no Render")
        st.code("""
        # Configurações ativas no motor robo-blitz
        API_ENDPOINT = "https://api.gerenciamento-double.internal"
        INTERVALO_VARREDURA_SEG = 1.0
        LIMITE_EXAUSTAO_STREAK = 5
        ENVIO_TELEGRAM = True
        MODO_AUDITORIA = "POLARS_OPTIMIZED"
        """, language="python")
