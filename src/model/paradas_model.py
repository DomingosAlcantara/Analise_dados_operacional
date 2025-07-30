"""Classe para modelagem das paradas de máquinas."""

import os
from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor

import pandas as pd

from src.uteis import Uteis


class ParadasModel(Uteis):
    """Classe para modelagem das paradas de máquinas."""

    def __init__(self, files_path):
        """Inicializa a classe com o DataFrame de paradas."""
        self._files_path = files_path

    def aplicar_filtros(self, df, filtros):
        """Aplica filtros ao DataFrame de paradas."""
        if not filtros:
            return df

        for coluna, valor in filtros.items():
            if coluna in df.columns:
                df = df[df[coluna].str.contains(valor, na=False)]

        return df

    # def _extrair_

    def _carregar_planilha(self, path):
        """Carrega uma planilha do Excel e retorna um DataFrame."""
        dtypes = {
            "Código MCU CTC": str,
            "Centro de Tratamento": str,
            "Nº Máquina de triagem": int,
            "Descrição da Falha": str,
        }
        try:
            df = pd.read_excel(
                path, skiprows=7, usecols=[0, 1, 2, 5, 6], dtype=dtypes
            )
            return df
        except ValueError as e:
            raise ValueError(f"Erro ao carregar a planilha: {path}") from e

    def _extrair_data(self, df):
        """Extrai a data do DataFrame de paradas."""
        df_data = df.copy()
        df_data["Data da Falha"] = df_data["Data/hora Inicial da Falha"].dt.date
        return df_data

    def _extrair_hora(self, df):
        """Extrai a hora do DataFrame de paradas."""
        df_hora = df.copy()
        df_hora["Hora da Falha"] = df_hora["Data/hora Inicial da Falha"].dt.time
        return df_hora

    def processar_dados(self):
        """Processa os arquivos de paradas e retorna um DataFrame consolidado."""

        if self._files_path:
            planilhas = os.listdir(self._files_path)
            caminhos = [os.path.join(self._files_path, p)
                        for p in planilhas if p.endswith('.xls')]

            with _ThreadPoolExecutor() as executor:
                dfs = list(executor.map(self._carregar_planilha, caminhos))

            if dfs:
                df_final = pd.concat(dfs, ignore_index=True)
                df_final = df_final.set_index("Código MCU CTC", drop=False)

                return df_final
