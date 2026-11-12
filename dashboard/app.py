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
    caminhos = [
        "double_history_auditado.parquet",
        "data/processed/double_history_auditado.parquet",
        "../double_history_auditado.parquet"
    ]
    for p in caminhos:
        if os.path.exists(p):
            return pl.read_parquet(p)
    st.error("Banco Parquet não encontrado. Execute a Fase 1 primeiro.")
    return None