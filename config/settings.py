# DOUBLE AI EVOLUTION - config/settings.py (v1.0)
from pathlib import Path

BASE_DIR = Path("/content/drive/MyDrive/DOUBLE_AI_EVOLUTION")
PROCESSED_PARQUET = BASE_DIR / "data" / "processed" / "double_history_auditado.parquet"
AUDIT_REPORT_CSV = BASE_DIR / "reports" / "fase1_auditoria_arquivos.csv"

SOURCE_FOLDERS = [
    "/content/drive/MyDrive/Histórico-2025",
    "/content/drive/MyDrive/Histórico-2025",
    "/content/drive/MyDrive/Histórico2022",
    "/content/drive/MyDrive/Histórico2022",
    "/content/drive/MyDrive/Históricoroleta1",
    "/content/drive/MyDrive/Históricoroleta1",
]

COLOR_TEXT_TO_ID = {"branco": 0, "vermelho": 1, "preto": 2, "white": 0, "red": 1, "black": 2, "0": 0, "1": 1, "2": 2}
COLOR_ID_TO_NAME = {0: "Branco", 1: "Vermelho", 2: "Preto"}
GAP_THRESHOLD_SECONDS = 300  # Acima de 5 minutos sem rodada marca quebra de sessão
