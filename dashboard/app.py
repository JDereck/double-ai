import streamlit as st
import polars as pl
import os
from pathlib import Path

# Configuração do diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

def carregar_dados():
    # Lista de caminhos possíveis para encontrar o banco Parquet
    caminhos = [
        "double_history_auditado.parquet",
        "data/processed/double_history_auditado.parquet",
        BASE_DIR / "data/processed/double_history_auditado.parquet",
        "../double_history_auditado.parquet"
    ]
    
    for p in caminhos:
        if os.path.exists(str(p)):
            return pl.read_parquet(str(p))
            
    st.error("Banco Parquet não encontrado. Execute a Fase 1 primeiro.")
    return None

# Carrega os dados para iniciar o painel
df = carregar_dados()
