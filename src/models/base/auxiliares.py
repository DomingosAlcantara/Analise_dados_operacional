"""
Esta classe contém as funções que auxiliaram o tratamento dos dados
"""

import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd


class Auxiliares:
    """
    Classe auxiliar para tratamento de dados.
    """

    def __init__(
        self, path: str, num_linhas_desconsiderar: int, utilizar_colunas: dict
    ) -> None:
        self._path = path
        self._num_linhas_desconsiderar = num_linhas_desconsiderar
        self._utilizar_colunas = utilizar_colunas

    def _carregar_planilha(self, caminho_do_arquivo) -> pd.DataFrame:
        """
        Carrega uma planilha Excel com configurações específicas.

        Returns:
            DataFrame: Dados carregados da planilha.
        """
        try:
            return pd.read_excel(
                caminho_do_arquivo,
                skiprows=self._num_linhas_desconsiderar,
                usecols=list(self._utilizar_colunas.keys()),
                dtype=self._utilizar_colunas,
            )
        except ValueError as e:
            raise ValueError(
                f"Erro ao carregar a planilha: {caminho_do_arquivo}"
            ) from e

    def _listar_arquivos(self) -> list:
        """
        Método placeholder para listar arquivos em um diretório.
        """
        # Implementar lógica para listar arquivos no diretório self._path
        return [
            f
            for f in os.listdir(self._path)
            if f.endswith(".xlsx") or f.endswith(".xls")
        ]

    def _listar_caminhos_arquivos(self) -> list:
        """
        Método para listar os caminhos completos dos arquivos no diretório.
        """
        arquivos = self._listar_arquivos()
        return [os.path.join(self._path, arquivo) for arquivo in arquivos]

    def _unir_planilhas(self, dataframes: list) -> pd.DataFrame:
        """
        Une múltiplos DataFrames em um único DataFrame.

        Args:
            dataframes (list): Lista de DataFrames a serem unidos.

        Returns:
            DataFrame: DataFrame resultante da união.
        """
        try:
            return pd.concat(dataframes, ignore_index=True)
        except ValueError:
            raise ValueError("No DataFrames to concatenate")

    def processar_dados(self):
        """
        Método placeholder para processamento de dados.
        """

        with ThreadPoolExecutor() as executor:
            dataframes = list(
                executor.map(
                    self._carregar_planilha,
                    self._listar_caminhos_arquivos(),
                )
            )
        return self._unir_planilhas(dataframes)
