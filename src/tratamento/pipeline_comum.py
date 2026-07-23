import pandas as pd


class Pipeline_Comum:

    @staticmethod
    def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza os nomes das colunas do DataFrame, convertendo para
        minúsculas e substituindo espaços por underscores.

        Args:
            df (pd.DataFrame): DataFrame a ser normalizado.

        Returns:
            pd.DataFrame: DataFrame com as colunas normalizadas.
        """
        df = df.copy()  # Cria uma cópia do DataFrame para evitar modificar o original
        if not df.columns.empty:
            df.columns = (
                df.columns.str.strip()
                .str.lower()
                .str.replace(" ", "_")
                .str.normalize("NFKD")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
            )
        return df

    @staticmethod
    def adicionar_abreviacoes_centros(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adiciona uma coluna 'abreviacao_centro_tratamento' ao DataFrame
        com base na coluna 'centro_de_tratamento'.

        Args:
            df (pd.DataFrame): DataFrame contendo a coluna
            'centro_de_tratamento'.

        Returns:
            pd.DataFrame: DataFrame com a nova coluna adicionada.
        """

        df = df.copy()  # Cria uma cópia do DataFrame para evitar modificar o original
        if not df.empty and "centro_de_tratamento" in df.columns:
            mapa_exibicao = {
                "CTCE SALVADOR": "CTCE<br>SALVADOR",
                "CTCE INDAIATUBA": "CTCE<br>INDAIATUBA",
                "CTCE JABOATAO DOS GUARARAPES": "CTCE\xa0JAB<br>GUARARAPES",
                # Adicione mais mapeamentos conforme necessário
            }

            df["centro_abrev_19"] = (
                df["centro_de_tratamento"]
                .map(mapa_exibicao)
                .fillna(df["centro_de_tratamento"].str[:19])
            )

            mapa_siglas = {
                "CTCE SALVADOR": "SDR",
                "CTCE INDAIATUBA": "IND",
                "CTCE JABOATAO DOS GUARARAPES": "JAB",
                # Adicione mais mapeamentos conforme necessário
            }
            df["centro_abrev_3"] = (
                df["centro_de_tratamento"].map(mapa_siglas).fillna("N/A")
            )
        return df
