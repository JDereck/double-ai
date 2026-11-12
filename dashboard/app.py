import streamlit as st
import polars as pl
import os
from pathlib import Path

# Configuração da Página
st.set_page_config(
    page_title="DOUBLE AI EVOLUTION",
    page_icon="🤖",
    layout="wide"
)

# Diretório base
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
st.title("🤖 DOUBLE AI EVOLUTION — Laboratório de IA & Auditoria")
st.markdown("---")

# Carrega os dados
df = carregar_dados()

if df is None:
    st.error("⚠️ Banco Parquet não encontrado. O arquivo 'double_history_auditado.parquet' precisa estar na raiz do projeto ou na pasta data/processed/.")
    st.info("Execute a Fase 1 no Colab para gerar ou verificar o banco de dados.")
else:
    st.success("✅ Banco Parquet carregado com sucesso!")
    
    # Métricas Principais
    total_linhas = len(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Rodadas Auditadas", f"{total_linhas:,}".replace(",", "."))
    with col2:
        st.metric("Status do Modelo", "Ativo & Operacional")
    with col3:
        st.metric("Versão do Motor", "v1.0 Cloud")
        
    st.markdown("### 📊 Prévia dos Dados Auditados")
    
    # Exibe amostra dos dados no formato Pandas para compatibilidade com Streamlit
    st.dataframe(df.head(100).to_pandas(), use_container_width=True)
    
    st.markdown("---")
    st.info("💡 Laboratório sincronizado com sucesso no Streamlit Cloud.")
