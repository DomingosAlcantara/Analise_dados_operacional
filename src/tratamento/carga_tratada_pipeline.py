import pandas as pd

from src.tratamento.pipeline_comum import Pipeline_Comum


class CargaTratadaPipeline:
    """Classe para tratar dados de carga tratada."""

    def __init__(self, df_bruto: pd.DataFrame):
        self._df_bruto = df_bruto.copy() if df_bruto is not None else pd.DataFrame()

    def remover_linhas_vazias(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove linhas vazias de um DataFrame.

        Args:
            df (DataFrame): DataFrame do qual as linhas vazias serão removidas.

        Returns:
            DataFrame: DataFrame sem linhas vazias.
        """
        return df.loc[
            df["quantidade_induzida"].notnull()
            & (df["quantidade_induzida"].fillna(0) != 0)
        ]  # noqa: E712

    def normalizar_datas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza as colunas de data do DataFrame, convertendo para o formato
        datetime.

        Args:
            df (DataFrame): DataFrame com colunas de data a serem normalizadas.

        Returns:
            DataFrame: DataFrame com colunas de data normalizadas.
        """
        df["data_de_triagem"] = pd.to_datetime(
            df["data_de_triagem"],
            format="%d/%m/%Y",
        )
        return df

    def processar(self) -> pd.DataFrame:
        if self._df_bruto.empty:
            return self._df_bruto

        return (
            self._df_bruto.pipe(Pipeline_Comum.normalizar_colunas)
            .pipe(self.remover_linhas_vazias)
            .pipe(self.normalizar_datas)
            .pipe(Pipeline_Comum.adicionar_abreviacoes_centros)
        )
