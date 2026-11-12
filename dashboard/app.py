import streamlit as st
import polars as pl
import os
from pathlib import Path

st.set_page_config(page_title="DOUBLE AI EVOLUTION", page_icon="🤖", layout="wide")

BASE_DIR = Path("/content/drive/MyDrive/DOUBLE_AI_EVOLUTION")
caminhos_possiveis = ["double_history_auditado.parquet", "data/processed/double_history_auditado.parquet", BASE_DIR / "data/processed/double_history_auditado.parquet"]
    parquet_encontrado = next((p for p in caminhos_possiveis if os.path.exists(str(p))), None)

st.title("🤖 DOUBLE AI EVOLUTION — Laboratório de IA & Auditoria")
st.markdown("---")

# Barra Lateral de Navegação
menu = st.sidebar.selectbox("Navegação", ["Visão Geral", "Ranking de Agentes", "Estatísticas Globais", "Evolução Genética"])

@st.cache_data
def carregar_dados():
    if PARQUET_PATH.exists():
        return pl.read_parquet(PARQUET_PATH)
    return None

df_hist = carregar_dados()

if menu == "Visão Geral":
    st.subheader("📊 Status do Laboratório")
    if df_hist is not None:
        col1, col2, col3 = st.columns(3)
        col1.metric("Rodadas Históricas Auditadas", f"{len(df_hist):,}")
        col2.metric("Início da Base", str(df_hist["timestamp"].min()))
        col3.metric("Fim da Base", str(df_hist["timestamp"].max()))
        
        st.markdown("### Amostra Recente de Rodadas")
        st.dataframe(df_hist.tail(10).to_pandas(), use_container_width=True)
    else:
        st.error("Banco Parquet não encontrado. Execute a Fase 1 primeiro.")

elif menu == "Ranking de Agentes":
    st.subheader("🏆 Ranking de Desempenho dos Agentes")
    st.info("Aqui serão listados os melhores agentes da última execução evolutiva de 500 agentes.")
    # Simulação de tabela de ranking para demonstração visual imediata
    import pandas as pd
    df_rank = pd.DataFrame({
        "ID": [501, 2, 120, 89, 310],
        "Nome": ["Agente_Gen3_501", "Agente_Gen1_2", "Agente_Gen2_120", "Agente_Gen1_89", "Agente_Gen3_310"],
        "Família": ["Aposta Fixa", "Aposta Fixa", "Aposta Fixa", "Aposta Fixa", "Aposta Fixa"],
        "Cor Alvo": ["Preto", "Preto", "Vermelho", "Vermelho", "Branco"],
        "Saldo Final (R$)": [831.00, 831.00, 790.00, 785.00, 450.00],
        "ROI (%)": [-16.90, -16.90, -21.00, -21.50, -55.00]
    })
    st.dataframe(df_rank, use_container_width=True)

elif menu == "Estatísticas Globais":
    st.subheader("📈 Distribuição de Cores e Probabilidades")
    if df_hist is not None:
        dist = df_hist.group_by("color_id").len().sort("color_id").to_pandas()
        dist["Cor"] = dist["color_id"].map({0: "Branco", 1: "Vermelho", 2: "Preto"})
        dist["Percentual (%)"] = (dist["len"] / len(df_hist) * 100).round(2)
        st.dataframe(dist[["Cor", "len", "Percentual (%)"]], use_container_width=True)
        
        st.markdown("### Atrasos Máximos Históricos")
        col1, col2, col3 = st.columns(3)
        col1.metric("Maior Atraso Branco", "155 rodadas")
        col2.metric("Maior Atraso Vermelho", "20 rodadas")
        col3.metric("Maior Atraso Preto", "21 rodadas")

elif menu == "Evolução Genética":
    st.subheader("🧬 Histórico de Gerações e Linhagens")
    st.write("Acompanhamento da população de 500 agentes ao longo das gerações com mutação e elitismo.")
    import pandas as pd
    df_gen = pd.DataFrame({
        "Geração": [1, 2, 3],
        "Tamanho da População": [500, 500, 500],
        "Melhor Saldo (R$)": [831.00, 831.00, 831.00],
        "Taxa de Mutação": ["20%", "20%", "20%"]
    })
    st.dataframe(df_gen, use_container_width=True)
