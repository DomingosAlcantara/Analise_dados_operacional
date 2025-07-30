"""Classe base para processamento de dados.
    """
import os
from abc import ABC

import pandas as pd


class Uteis(ABC):
    """Classe utilitária para operações comuns de processamento de dados.
    """

    def __init__(self, dados) -> None:
        self._set_dados(dados)
        self._data = None

    def _set_dados(self, dados):
        """Define os dados a serem processados."""
        if dados is not None:
            self._data = dados.copy()
        else:
            self._data = None

    def get_dados(self):
        """Retorna os dados processados."""
        if self._data is not None:
            return self._data
        else:
            raise ValueError("Dados não carregados.")

    def carregar_planilha(self, path):
        """Carrega uma planilha do Excel e retorna um DataFrame."""
        try:
            df = pd.read_excel(path, skiprows=8)
            return df
        except ValueError as e:
            raise ValueError(f"Erro ao carregar a planilha: {path}") from e

    def recuperar_dados_pelo_centro(self, centro: str):
        """
        Recupera os dados filtrados pelo centro de triagem.
        """
        df = self.get_dados()
        if df is not None:
            return df[df["Centro de Tratamento"] == centro.upper()]
        else:
            raise ValueError("Dados não carregados.")

    def _recuperar_caminho_das_planilhas(self, files_path):
        """
        Recupera os caminhos das planilhas no diretório especificado.
        """
        return [os.path.join(files_path, f) for f in os.listdir(files_path)
                if f.endswith('.xls')]

    # @abstractmethod
    # def carregar_planilha(self, path):
    #     '''
    #     Carrega uma planilha do Excel e retorna um DataFrame.
    #     '''
