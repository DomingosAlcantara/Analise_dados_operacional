""" Esta classe encapsula a lógica de processamento dos dados de atolamentos,
    incluindo a soma de cargas tratadas e falhas técnicas.
"""
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd
from pandas import DataFrame

from uteis import Uteis


class ParadasModel(Uteis):
    """
    Classe para gerenciar os dados de atolamentos.
    """

    def __init__(self, path="/home/domingos/Documentos/Dados/Engarrafamento/"):
        self._file_path = path
        self.processar_dados()

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

    def processar_dados(self) -> None:
        """
        Processa os arquivos de atolamentos e retorna um DataFrame consolidado.

        Returns:
            DataFrame: Dados consolidados dos atolamentos.
        """
        files = [f for f in os.listdir(self._file_path) if f.endswith('.xls')]
        dataframes = []
        df_dados = None

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
            df_dados = pd.concat(dataframes, ignore_index=True)
            df_dados = pipeline(df_dados)
            df_dados.set_index("código_mcu_ctc", inplace=True)
            self._set_dados(df_dados)
        else:
            raise ValueError("Nenhum dado foi carregado.")

    def _get_maiores_atolamentos(self, n: int = 5) -> DataFrame:
        """
        Retorna os maiores atolamentos.

        Args:
            n (int): Número de maiores atolamentos a serem retornados.

        Returns:
            DataFrame: DataFrame contendo os maiores atolamentos.
        """
        df_dados = self.get_dados().copy()
        tops = df_dados["descrição_da_falha"].value_counts().head(n).\
            reset_index()
        tops.columns = ["descrição_da_falha", "quantidade"]
        return tops

    def soma_total_atolamentos(self) -> int:
        """
        Retorna a soma total de atolamentos.

        Returns:
            int: Soma total de atolamentos.
        """
        df_dados = self.get_dados()
        return df_dados.shape[0] if df_dados is not None else 0

    def get_atolamentos_em_percentual(self,
                                      top_atolamentos: int = 5) -> DataFrame:
        """
        Retorna o percentual de atolamentos por máquina.

        Returns:
            DataFrame: DataFrame contendo o percentual de atolamentos.
        """
        df_dados = self._get_maiores_atolamentos(top_atolamentos)
        total_atolamentos = self.soma_total_atolamentos()
        if total_atolamentos == 0:
            return pd.DataFrame(columns=["descrição_da_falha",
                                         "quantidade", "percentual"])

        df_dados["percentual"] = (df_dados["quantidade"] /
                                  total_atolamentos) * 100
        return df_dados

    def mostrar_maquinas(self) -> DataFrame:
        """
        Retorna as máquinas existentes no Centro de Tratamento.

        Returns:
            DataFrame: DataFrame contendo as máquinas.
        """
        df_dados = self.get_dados()
        maquinas = df_dados["nº_máquina_de_triagem"].unique()
        return pd.DataFrame(maquinas, columns=["nº_máquina_de_triagem"])
