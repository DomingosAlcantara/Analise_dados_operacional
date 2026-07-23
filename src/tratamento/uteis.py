import pandas as pd


class Uteis:
    """
    Classe utilitária para fornecer métodos auxiliares.
    """

    def normalizar_colunas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza os nomes das colunas do DataFrame, convertendo para
        minúsculas e substituindo espaços por underscores.

        Args:
            df (pd.DataFrame): DataFrame a ser normalizado.

        Returns:
            pd.DataFrame: DataFrame com as colunas normalizadas.
        """
        if df is not None and not df.empty:
            df.columns = (
                df.columns.str.strip()
                .str.lower()
                .str.replace(" ", "_")
                .str.normalize("NFKD")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
            )
        return df

    def adicionar_coluna_abreviacao_centro_tratamento(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Adiciona uma coluna 'abreviacao_centro_tratamento' ao DataFrame
        com base na coluna 'centro_de_tratamento'.

        Args:
            df (pd.DataFrame): DataFrame contendo a coluna
            'centro_de_tratamento'.

        Returns:
            pd.DataFrame: DataFrame com a nova coluna adicionada.
        """

        mapa_centros = {
            "CTCE SALVADOR": "SDR",
            "CTCE INDAIATUBA": "IND",
            "CTCE JABOATAO DOS GUARARAPES": "JAB",
            # Adicione mais mapeamentos conforme necessário
        }

        if "centro_de_tratamento" in df.columns:
            valores = df["centro_de_tratamento"]
        return df
