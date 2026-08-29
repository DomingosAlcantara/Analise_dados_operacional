import pandas as pd

# from src.utils.cache import cache


class FalhasTecnicasModel:
    """
    Classe para gerenciar os dados de falhas técnicas.
    """

    def __init__(self, df_dados: pd.DataFrame):
        self._dados = df_dados.copy() if df_dados is not None else pd.DataFrame()
        self._dados_filtrados = self._dados.copy()

    def filtrar_dados_por_data(self, data_inicial, data_final):
        """
        Filtra os dados de falhas técnicas por um intervalo de datas.

        Args:
            data_inicial (str): Data inicial no formato 'YYYY-MM-DD'.
            data_final (str): Data final no formato 'YYYY-MM-DD'.

        Returns:
            DataFrame: Dados filtrados pelo intervalo de datas.
        """
        try:
            start = pd.to_datetime(data_inicial, dayfirst=False).date()
            end = pd.to_datetime(data_final, dayfirst=False).date()

            mascara = self._dados["data_da_falha"].between(start, end)
            self._dados_filtrados = self._dados.loc[mascara].copy()

        except Exception:
            self._dados_filtrados = pd.DataFrame()

        return self

    def retornar_falhas_por_centro(self):
        """
        Retorna o total de falhas agrupadas por centro

        Returns:
            pd.DataFrame: DataFrame contendo 'centro_de_tratamento' e 'total_de_falhas'
            ordenado do maior para o menor
        """

        if self._dados_filtrados.empty:
            return pd.DataFrame(columns=["centro_de_tratamento", "total_de_falhas"])

        return (
            self._dados_filtrados.groupby("centro_de_tratamento")
            .size()
            .reset_index(name="total_de_falhas")
            .sort_values(by="total_de_falhas", ascending=False)
        )

    def total_falhas_tecnicas(self) -> int:
        """
        Retorna o total de falhas técnicas.

        Returns:
            int: Total de falhas técnicas.
        """
        return int(self._dados_filtrados.shape[0])  # ["descrição_da_falha"].count()

    def retornar_metricas_falhas_tecnicas(self, data_inicial, data_final):
        """
        Retorna as métricas relacionadas às falhas técnicas.

        Returns:
            dict: Dicionário contendo as métricas calculadas.
        """
        self.filtrar_dados_por_data(data_inicial, data_final)

        return {
            "total_de_falhas": self.total_falhas_tecnicas(),
            # "media_objetos_por_falha": round(self.media_objetos_por_falhas(), 2),
            "tempo_total_ocorrencias": 0,
            "duracao_media_falha": 0,
        }
