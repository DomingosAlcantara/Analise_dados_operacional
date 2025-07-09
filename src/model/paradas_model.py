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

    def processar_dados(self):
        """Processa os arquivos de paradas e retorna um DataFrame consolidado."""

        def carregar_planilha(path):
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

        if self._files_path:
            planilhas = os.listdir(self._files_path)
            caminhos = [os.path.join(self._files_path, p)
                        for p in planilhas if p.endswith('.xls')]

            with _ThreadPoolExecutor() as executor:
                dfs = list(executor.submit(carregar_planilha, caminho)
                           for caminho in caminhos)
