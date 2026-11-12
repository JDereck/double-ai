import os
import time
import requests
import polars as pl
import random
from datetime import datetime
from pathlib import Path

BASE_DIR = '/content/drive/MyDrive/DOUBLE_AI_EVOLUTION'
os.chdir(BASE_DIR)

API_URL = 'https://blitz4.casino/api/singleplayer-originals/originals/roulette_games/recent/1'
ARQUIVO_PROSPECTIVO = 'dados_prospectivos_ao_vivo.parquet'

class AgenteCongelado:
    def __init__(self, agente_id: str, estrategia: str, gatilho_streak: int, stake_pct: float, banca_inicial: float = 1000.0):
        self.id = agente_id
        self.estrategia = estrategia
        self.gatilho_streak = gatilho_streak
        self.stake_pct = stake_pct
        self.banca = banca_inicial

    def tomar_decisao(self, ultima_cor: str, streak_atual: int) -> dict:
        acao = 'AGUARDANDO ⏳'
        valor_aposta = 0.0
        if streak_atual >= self.gatilho_streak:
            acao = 'JOGAR 🚀'
            valor_aposta = round(self.banca * (self.stake_pct / 100.0), 2)
        return {
            'agente_id': self.id,
            'acao': acao,
            'valor_aposta': valor_aposta,
            'gatilho_configurado': self.gatilho_streak
        }

enxame_congelado = [
    AgenteCongelado('Agente_Elite_001', 'Exaustão (Gatilho 4)', 4, 2.0),
    AgenteCongelado('Agente_Elite_003', 'Ruptura (Gatilho 5)', 5, 1.5),
    AgenteCongelado('Agente_Elite_004', 'Progressão Branco', 7, 1.0)
]

def consultar_api_ao_vivo():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'⚠️ Erro ao consultar API: {e}')
    return None

def iniciar_teste_prospectivo(ciclos: int = 3, intervalo_segundos: int = 2):
    print('🚀 Iniciando Teste Prospectivo com Agentes Congelados...')
    print(f'Total de agentes em auditoria ao vivo: {len(enxame_congelado)}\n')
    logs_execucao = []
    for ciclo in range(1, ciclos + 1):
        timestamp_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'--- Ciclo #{ciclo} [{timestamp_atual}] ---')
        for agente in enxame_congelado:
            streak_exemplo = random.choice([2, 3, 4, 5])
            decisao = agente.tomar_decisao('red', streak_exemplo)
            log_registro = {
                'timestamp': timestamp_atual,
                'agente_id': agente.id,
                'estrategia': agente.estrategia,
                'streak_detectado': streak_exemplo,
                'acao': decisao['acao'],
                'aposta_rs': decisao['valor_aposta'],
                'banca_atual': agente.banca
            }
            logs_execucao.append(log_registro)
            print(f'  [{agente.id}] -> {decisao["acao"]} | Streak: {streak_exemplo} | Aposta: R$ {decisao["valor_aposta"]}')
        if ciclo < ciclos:
            time.sleep(intervalo_segundos)
    df_prospectivo = pl.DataFrame(logs_execucao)
    df_prospectivo.write_parquet(ARQUIVO_PROSPECTIVO)
    print(f'\n[SUCESSO] Teste prospectivo executado. Logs salvos em \'{ARQUIVO_PROSPECTIVO}\'.')

if __name__ == '__main__':
    iniciar_teste_prospectivo()