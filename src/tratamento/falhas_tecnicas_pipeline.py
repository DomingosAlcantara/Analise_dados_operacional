import pandas as pd

from src.tratamento.pipeline_comum import Pipeline_Comum


class FalhasTecnicasPipeline:
    """
    Pipeline para processar falhas técnicas.
    """

    def __init__(self, df_bruto: pd.DataFrame):
        self._df_bruto = df_bruto.copy() if df_bruto is not None else pd.DataFrame()

    def remover_desabilitacoes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove registros de falhas técnicas que correspondem a desabilitações.

        Returns:
            pd.DataFrame: DataFrame com os registros filtrados.
        """
        _df = df.copy()  # Cria uma cópia do DataFrame para evitar modificar o original

        return _df.loc[
            _df["descricao_da_falha"]
            != "Máquina desabilitada - pressione e mantenha o botão de habilitar por 1 segundo p"
        ]
        # return self

    def renomear_colunas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Renomeia as colunas do DataFrame de falhas técnicas.

        Returns:
            pd.DataFrame: DataFrame com as colunas renomeadas.
        """
        if df.empty:
            return df

        return df.rename(
            columns={
                "no_maquina_de_triagem": "no_maquina",
            }
        )
        # return df

    def processar(self) -> pd.DataFrame:
        """
        Processa o DataFrame de falhas técnicas.

        Args:
            df (pd.DataFrame): DataFrame de falhas técnicas a ser processado.

        Returns:
            pd.DataFrame: DataFrame processado.
        """
        # Aqui você pode adicionar qualquer lógica de processamento necessária
        if self._df_bruto.empty:
            return self._df_bruto

        return (
            self._df_bruto.pipe(Pipeline_Comum.normalizar_colunas)
            .pipe(self.remover_desabilitacoes)
            .pipe(self.renomear_colunas)
            .pipe(Pipeline_Comum.adicionar_abreviacoes_centros)
        )

        # self.normalizar_colunas().remover_desabilitacoes().renomear_colunas()

        # return self.df_falhas_tecnicas
