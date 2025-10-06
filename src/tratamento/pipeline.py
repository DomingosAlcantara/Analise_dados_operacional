import pandas as pd


class Pipeline:
    def __init__(self, dataframe: pd.DataFrame, transformacoes: list):
        """Classe para aplicar as transformações no DataFrame informado.

        Args:
            dataframe (DataFrame): Dados onde as transformações serão
            aplicadas.
            transformacoes (list): As trasnformações que serão aplicadas nos
            dados.
        """
        self._dataframe = dataframe.copy(
            deep=True) if dataframe is not None else None
        self._transformacoes = list(
            transformacoes) if transformacoes is not None else []

    def aplicar_transformacoes(self):
        if self._dataframe is None:
            raise ValueError("DataFrame não fornecido")

        if not self._transformacoes:
            raise ValueError("Transformações não fornecidas")

        df_tratado = pd.DataFrame()
        for transformacao in self._transformacoes:
            if hasattr(self, transformacao):
                func = getattr(self, transformacao)
                df_tratado = func(self._dataframe)
            else:
                raise ValueError(
                    f"Transformação '{transformacao}' não encontrada")

        return df_tratado
