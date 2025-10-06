from datetime import datetime

import pandas as pd

from src.extracoes.extracoes import Extracoes
from src.path_files import PathFiles
from src.tratamento.pipeline import Pipeline


class Parada(Extracoes):
    """
    Classe para carregar e validar dados de engarrafamento.
    """

    def __init__(self):
        super().__init__(PathFiles.ARQUIVOS_ATOLAMENTOS)

    def padronizar_colunas(self, df: pd.DataFrame) -> pd.DataFrame:
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

    def remover_desabilitacoes(self, df: pd.DataFrame) -> pd.DataFrame:
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

    def extrair_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extrai a data e hora da coluna de data/hora inicial do atolamento.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com as colunas de data e hora extraídas.
        """
        df["Data da Falha"] = df["Data/hora inicial da Falha"].dt.date
        return df

    def extrair_hora(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extrai a hora da coluna de data/hora inicial do atolamento.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com a coluna de hora extraída.
        """
        df["Hora da Falha"] = df["Data/hora inicial da Falha"].dt.time
        return df

    def remover_coluna_de_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove a coluna de data do DataFrame.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame sem a coluna de data.
        """
        if "Data/hora inicial do Atolamento" in df.columns:
            df.drop(columns=["Data/hora inicial da Falha"], inplace=True)
        return df

    def processar_pasta(self) -> pd.DataFrame:
        """
        Processa os dados de engarrafamento a partir dos arquivos
        Excel no diretório especificado.

        Returns:
            DataFrame: Lista de DataFrames contendo os dados carregados.
        """
        df_bruto = self.processar_arquivos(
            path_files=self.construir_caminhos_completos(
                self.listar_arquivos()),
            colunas_tipo={
                "data/hora_inicial_da_falha": datetime,
                "codigo_mcu_ctc": int,
                "centro_de_tratamento": str,
                "nº_máquina_de_triagem": int,
                "descricao_da_falha": str,
            },
            linhas_para_pular=7
        )

        pipe = Pipeline(dataframe=df_bruto, transformacoes=[
            self.padronizar_colunas,
            self.remover_desabilitacoes,
            self.extrair_data,
            self.extrair_hora,
            self.remover_coluna_de_data,
        ])

        return pipe.aplicar_transformacoes()
