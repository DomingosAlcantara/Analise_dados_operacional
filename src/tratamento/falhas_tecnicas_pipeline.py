import pandas as pd

from src.tratamento.uteis import Uteis


class FalhasTecnicasPipeline:
    """
    Pipeline para processar falhas técnicas.
    """

    def __init__(self):
        self.uteis = Uteis()

    def normalizar_colunas(self) -> "FalhasTecnicasPipeline":
        """
        Normaliza os nomes das colunas do DataFrame, convertendo para
        minúsculas e substituindo espaços por underscores.

        Returns:
            PipelineFalhasTecnicas: Pipeline com o DataFrame normalizado.
        """
        self.df_falhas_tecnicas = self.uteis.normalizar_colunas(self.df_falhas_tecnicas)
        return self

    def remover_desabilitacoes(self) -> "FalhasTecnicasPipeline":
        """
        Remove registros de falhas técnicas que correspondem a desabilitações.

        Returns:
            PipelineFalhasTecnicas: Pipeline com o DataFrame filtrado.
        """
        if self.df_falhas_tecnicas.empty:
            return self
        print(
            f"Normalizando colunas do DataFrame de falhas técnicas: {self.df_falhas_tecnicas.columns.tolist()}"
        )

        self.df_falhas_tecnicas = self.df_falhas_tecnicas.loc[
            self.df_falhas_tecnicas["descricao_da_falha"]
            != "Máquina desabilitada - pressione e mantenha o botão de habilitar por 1 segundo p"
        ]
        return self

    def renomear_colunas(self) -> "FalhasTecnicasPipeline":
        """
        Renomeia as colunas do DataFrame de falhas técnicas.

        Returns:
            PipelineFalhasTecnicas: Pipeline com o DataFrame com colunas renomeadas.
        """
        if self.df_falhas_tecnicas.empty:
            return self

        self.df_falhas_tecnicas = self.df_falhas_tecnicas.rename(
            columns={
                "no_maquina_de_triagem": "no_maquina",
            }
        )
        return self

    def processar(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processa o DataFrame de falhas técnicas.

        Args:
            df (pd.DataFrame): DataFrame de falhas técnicas a ser processado.

        Returns:
            pd.DataFrame: DataFrame processado.
        """
        # Aqui você pode adicionar qualquer lógica de processamento necessária
        if df.empty:
            return df

        self.df_falhas_tecnicas = df.copy()

        self.normalizar_colunas().remover_desabilitacoes().renomear_colunas()

        return self.df_falhas_tecnicas
