import polars as pl
import numpy as np
from scipy import stats

class StatisticalLaboratory:
    def __init__(self, parquet_path):
        self.df = pl.read_parquet(parquet_path)

    def analisar_distribuicao_global(self):
        total = len(self.df)
        contagens = self.df.group_by("color_id").len().sort("color_id")
        
        # Frequências teóricas: Branco(0) = 1/15 (6.6667%), Vermelho(1) = 7/15 (46.6667%), Preto(2) = 7/15 (46.6667%)
        freqs_obs = contagens["len"].to_numpy()
        freqs_esp = np.array([total * (1/15), total * (7/15), total * (7/15)])
        
        chi2, p_val = stats.chisquare(freqs_obs, f_exp=freqs_esp)
        return contagens, chi2, p_val

    def calcular_atrasos_maximos(self):
        # Calcula a sequência máxima consecutiva sem sair cada cor
        df_pd = self.df.select(["color_id"]).to_pandas()
        atrasos = {}
        for cor_id, nome in [(0, "Branco"), (1, "Vermelho"), (2, "Preto")]:
            mask = (df_pd["color_id"] != cor_id).astype(int)
            # Grupos de ocorrências consecutivas sem a cor
            grupos = mask.groupby((mask != mask.shift()).cumsum()).sum()
            atrasos[nome] = int(grupos.max()) if not grupos.empty else 0
        return atrasos
