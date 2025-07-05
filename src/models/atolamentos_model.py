""" Esta classe encapsula a lógica de processamento dos dados de atolamentos,
    incluindo a soma de cargas tratadas e falhas técnicas.
"""
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd
from pandas import DataFrame

from uteis import Uteis


class AtolamentoModel(Uteis):
    """
    Classe para gerenciar os dados de atolamentos.
    """

    def __init__(self, path="/home/domingos/Documentos/Dados/Engarrafamento/"):
        self._file_path = path
        self._dados = None

    def carregar_planilha(self, path) -> DataFrame:
        """
            Carrega a planilha de dados de atolamentos.

        Args:
            path (str): Caminho para o arquivo da planilha.

        Returns:
            DataFrame: Dados carregados da planilha.
        """
        dtypes = {
            "Código MCU CTC": str,
            "Centro de Tratamento": str,
            "Nº Máquina de triagem": int,
            "Descrição da Falha": str,
            "Data/hora inicial do Atolamento": datetime
        }

        try:
            df = pd.read_excel(path, skiprows=7, usecols=[
                0, 1, 2, 5, 6], dtype=dtypes)
            return df
        except ValueError:
            raise ValueError(f"Erro ao carregar a planilha: {path}")

    def padronizar_colunas(self, df: DataFrame) -> DataFrame:
        """
        Padroniza os nomes das colunas do DataFrame.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com as colunas padronizadas.
        """
        df.columns = [col.strip().lower().replace(" ", "_")
                      for col in df.columns]
        return df

    def remover_desabilitacoes(self, df: DataFrame) -> DataFrame:
        """
        Filtra o DataFrame de atolamentos com base em critérios específicos.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame filtrado.
        """
        # Exemplo de filtro, ajuste conforme necessário
        df = df[df["Descrição da Falha"] != "Máquina desabilitada - pressione \
            e mantenha o botão de habilitar por 1 segundo p"]
        return df

    def converter_para_datetime(self, df: DataFrame) -> DataFrame:
        """
        Converte a coluna de data/hora inicial do atolamento para o tipo
        datetime.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com a coluna convertida.
        """
        df["Data/hora inicial do Atolamento"] = pd.to_datetime(
            df["Data/hora inicial do Atolamento"],
            format="%d/%m/%Y %H:%M:%S"  # ajuste o formato conforme necessário
        )
        return df

    def extrair_data(self, df: DataFrame) -> DataFrame:
        """
        Extrai a data e hora da coluna de data/hora inicial do atolamento.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com as colunas de data e hora extraídas.
        """
        df["Data da Falha"] = df["Data/hora inicial do Atolamento"].dt.date
        return df

    def extrair_hora(self, df: DataFrame) -> DataFrame:
        """
        Extrai a hora da coluna de data/hora inicial do atolamento.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com a coluna de hora extraída.
        """
        df["Hora da Falha"] = df["Data/hora inicial do Atolamento"].dt.time
        return df

    def remover_coluna_de_data(self, df: DataFrame) -> DataFrame:
        """
        Remove a coluna de data do DataFrame.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame sem a coluna de data.
        """
        if "Data/hora inicial do Atolamento" in df.columns:
            df.drop(columns=["Data/hora inicial do Atolamento"], inplace=True)
        return df

    def processar_dados(self) -> DataFrame:
        """
        Processa os arquivos de atolamentos e retorna um DataFrame consolidado.

        Returns:
            DataFrame: Dados consolidados dos atolamentos.
        """
        files = [f for f in os.listdir(self._file_path) if f.endswith('.xlsx')]
        dataframes = []

        def pipeline(df: DataFrame) -> DataFrame:
            df = self.remover_desabilitacoes(df)
            df = self.converter_para_datetime(df)
            df = self.extrair_data(df)
            df = self.extrair_hora(df)
            df = self.remover_coluna_de_data(df)
            df = self.padronizar_colunas(df)
            return df

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.carregar_planilha, os.path.join(
                self._file_path, file)) for file in files]
            for future in futures:
                try:
                    df = future.result()
                    dataframes.append(df)
                except Exception as e:
                    print(f"Erro ao processar o arquivo: {e}")

        if dataframes:
            self._dados = pd.concat(dataframes, ignore_index=True)
            self._dados = pipeline(self._dados)
            self._dados.set_index("código_mcu_ctc", inplace=True)
            return self._dados
        else:
            raise ValueError("Nenhum dado foi carregado.")

    def get_dados(self) -> DataFrame:
        """
        Retorna os dados de atolamentos processados.

        Returns:
            DataFrame: Dados de atolamentos.
        """

        if self._dados is None:
            self.processar_dados()
        if self._dados is None:
            raise ValueError("Os dados de atolamentos não foram carregados.")
        return self._dados

    def get_maiores_atolamentos(self, n: int = 5) -> DataFrame:
        """
        Retorna os maiores atolamentos.

        Args:
            n (int): Número de maiores atolamentos a serem retornados.

        Returns:
            DataFrame: DataFrame contendo os maiores atolamentos.
        """
        if self._dados is None:
            self._dados = self.get_dados()
        tops = self._dados["descrição_da_falha"].value_counts().head(n).\
            reset_index()
        tops.columns = ["descrição_da_falha", "quantidade"]
        return tops
