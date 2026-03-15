"""Esta classe encapsula a lógica de processamento dos dados de atolamentos,
incluindo a soma de cargas tratadas e falhas técnicas.
"""

import pandas as pd
from pandas import DataFrame

from src.models.base.auxiliares import Auxiliares
from src.uteis import Uteis


class ParadasModel(Uteis):
    """
    Classe para gerenciar os dados de atolamentos.
    """

    def __init__(self, path="/home/domingos/Documentos/Dados/Engarrafamento/"):
        self._linhas_desconsiderar = 7
        self._colunas_utilizar = {
            "Código MCU CTC": str,
            "Centro de Tratamento": str,
            "Nº Máquina de triagem": int,
            "Descrição da Falha": str,
            "Data/hora inicial da Falha": str,
            "Data/hora final da Falha": str,
        }

        self._auxiliares = Auxiliares(
            str(path), self._linhas_desconsiderar, self._colunas_utilizar
        )
        self._set_dados(self._auxiliares.processar_dados())
        self._dados_filtrados = pd.DataFrame()

    def padronizar_colunas(self, df: DataFrame) -> DataFrame:
        """
        Padroniza os nomes das colunas do DataFrame.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com as colunas padronizadas.
        """
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
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
        df = df.loc[
            df["Descrição da Falha"]
            != "Máquina desabilitada - pressione e mantenha o botão de habilitar por 1 segundo p"
        ]
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
        df = df.copy()
        df["Data/hora inicial da Falha"] = pd.to_datetime(
            df["Data/hora inicial da Falha"],
            format="%d/%m/%Y %H:%M:%S",  # ajuste o formato conforme necessário
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
        df = df.copy()
        df["Data da Falha"] = df["Data/hora inicial da Falha"].dt.date
        return df

    def extrair_hora(self, df: DataFrame) -> DataFrame:
        """
        Extrai a hora da coluna de data/hora inicial do atolamento.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame com a coluna de hora extraída.
        """
        df = df.copy()
        df["Hora da Falha"] = df["Data/hora inicial da Falha"].dt.time
        return df

    def remover_coluna_de_data(self, df: DataFrame) -> DataFrame:
        """
        Remove a coluna de data do DataFrame.

        Args:
            df (DataFrame): DataFrame contendo os dados de atolamentos.

        Returns:
            DataFrame: DataFrame sem a coluna de data.
        """
        df = df.copy()
        if "Data/hora inicial da Falha" in df.columns:
            df.drop(columns=["Data/hora inicial da Falha"], inplace=True)
        return df

    def get_maiores_paradas(self, n: int = 5) -> DataFrame:
        """
        Retorna os maiores atolamentos.

        Args:
            n (int): Número de maiores atolamentos a serem retornados.

        Returns:
            DataFrame: DataFrame contendo os maiores atolamentos.
        """
        df_dados = self.get_dados().copy()
        tops = df_dados["descrição_da_falha"].value_counts().head(n).reset_index()
        tops.columns = ["descrição_da_falha", "quantidade"]
        return tops

    def get_soma_total_paradas(self) -> int:
        """
        Retorna a soma total de atolamentos.

        Returns:
            int: Soma total de atolamentos.
        """
        df_dados = self.get_dados()
        return df_dados.shape[0] if df_dados is not None else 0

    def get_paradas_em_percentual(self, top_paradas: int = 5) -> DataFrame:
        """
        Retorna o percentual de atolamentos por máquina.

        Returns:
            DataFrame: DataFrame contendo o percentual de atolamentos.
        """
        df_dados = self.get_maiores_paradas(top_paradas)
        total_paradas = self.get_soma_total_paradas()
        if total_paradas == 0:
            return pd.DataFrame(
                columns=["descrição_da_falha", "quantidade", "percentual"]
            )

        df_dados["percentual"] = (df_dados["quantidade"] / total_paradas) * 100
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
