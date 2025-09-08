"""Classe base para processamento de dados.
    """
from abc import ABC
from datetime import datetime

import pandas as pd
from pandas import DataFrame


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

    def _formatar_datas(self, data):
        """Formata a data no formato desejado."""
        # Formato desejado: "09072024" -> "2024-09-07"
        return datetime.strptime(data, "%m%d%Y").date()

    def _is_single_date(self, value, date_format="%d/%m/%Y"):
        """Verifica se o valor é uma data única."""
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            return False

    def _is_date_range(self, value, date_format="%d/%m/%Y"):
        """Verifica se o valor é um intervalo de datas."""
        try:
            start_date, end_date = value.split(" - ")
            return self._is_single_date(start_date, date_format) and \
                self._is_single_date(end_date, date_format)
        except ValueError:
            return False

    def recuperar_dados_pelo_centro(self, centro: str):
        """
        Recupera os dados filtrados pelo centro de triagem.
        """
        df = self.get_dados()
        if df is not None:
            return df[df["Centro de Tratamento"] == centro.upper()]
        else:
            raise ValueError("Dados não carregados.")

    def _carregar_planilha(self, path, linhas_para_pular=0,
                           usar_colunas: list = [],
                           tipos_colunas: dict = {}) -> DataFrame:
        '''
        Carrega uma planilha do Excel e retorna um DataFrame.
        '''
        try:
            df = pd.read_excel(
                path,
                skiprows=linhas_para_pular,
                usecols=usar_colunas,
                dtype=tipos_colunas
            )

            return df
        except ValueError:
            raise ValueError(f"Erro ao carregar a planilha: {path}")

    def _extrair_colunas_informadas(self, d_colunas: dict) -> list:
        """
        Extrai as colunas informadas no dicionário.
        """
        return list(d_colunas.keys())

    def _pipeline(self, df: DataFrame, funcoes: list) -> DataFrame:
        """
        Aplica uma série de funções em pipeline ao DataFrame.
        """

        # Caso base: Se a lista de funções estiver vazia, retorna o DataFrame
        if not funcoes:
            return df

        # Passo Recursivo:
        # Pega a primeira função da lista
        primeira_função = funcoes[0]
        # Pega o restante das funçoes
        funcoes_restantes = funcoes[1:]

        # Aplica a primeira função ao DataFrame
        df = primeira_função(df)
        return self._pipeline(df, funcoes_restantes)
