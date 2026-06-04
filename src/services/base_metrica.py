import pandas as pd


class BaseMetrica:
    """
    Classe base para métricas relacionadas à carga induzida e rendimento efetivo.
    Esta classe pode ser estendida para incluir métodos específicos de cálculo
    de métricas, como média diária de carga induzida, rendimento efetivo médio,
    entre outros.
    """

    def __init__(self, df_bruto: pd.DataFrame):
        """Inicializa a classe com um DataFrame contendo os dados necessários
        para o cálculo das métricas.

        Args:
            df (pd.DataFrame): DataFrame contendo os dados dos centros de
            tratamento, máquinas e cargas induzidas.
        """
        self._df_bruto = df_bruto
        self._df = df_bruto

    def filtrar(self, data_inicial, data_final):
        """Filtra o DataFrame com base em um intervalo de datas.

        Args:
            data_inicial (str): Data inicial no formato 'YYYY-MM-DD'.
            data_final (str): Data final no formato 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: DataFrame filtrado com os dados dentro do intervalo
            de datas.
        """
        self._df = self._df_bruto[
            (self._df_bruto["data_de_triagem"].between(data_inicial, data_final))
        ]
