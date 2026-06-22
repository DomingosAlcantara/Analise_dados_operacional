import pandas as pd


class CargaTratadaPipeline:
    """Classe para tratar dados de carga tratada."""

    def __init__(self):
        self._df = pd.DataFrame()

    def processar(self, df: pd.DataFrame):
        if df.empty:
            return df

        self._df = df.copy()

        self.normalizar_colunas().remover_linhas_vazias().normalizar_datas()

        return self._df

    def normalizar_colunas(self):
        """Normaliza os nomes das colunas do DataFrame, convertendo para
        minúsculas e substituindo espaços por underscores.
        """
        self._df.columns = (
            self._df.columns.str.strip().str.lower().str.replace(" ", "_")
        )
        return self

    def remover_linhas_vazias(self):
        """
        Remove linhas vazias de um DataFrame.

        Args:
            df (DataFrame): DataFrame do qual as linhas vazias serão removidas.

        Returns:
            DataFrame: DataFrame sem linhas vazias.
        """
        self._df = self._df.loc[
            self._df["quantidade_induzida"].notnull()
            & (self._df["quantidade_induzida"].fillna(0) != 0)
        ]  # noqa: E712
        return self

    def normalizar_datas(self):
        """
        Normaliza as colunas de data do DataFrame, convertendo para o formato
        datetime.

        Args:
            df (DataFrame): DataFrame com colunas de data a serem normalizadas.

        Returns:
            DataFrame: DataFrame com colunas de data normalizadas.
        """
        self._df["data_de_triagem"] = pd.to_datetime(
            self._df["data_de_triagem"],
            format="%d/%m/%Y",
        )
        return self
