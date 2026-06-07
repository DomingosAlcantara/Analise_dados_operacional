"""Classe para modelagem da carga induzida nas máquinas de triagem
automatizadas nos Centros de Tratamento.
"""

import pandas as pd

from src.utils.cache import cache


class CargaInduzidaModel:
    """
    Classe base para modelagem da carga induzida.
    Esta classe pode ser estendida para incluir atributos e métodos específicos
    relacionados à carga induzida nas máquinas de triagem nos centros de
    tratamento.
    """

    def __init__(self, df_dados: pd.DataFrame):
        self._df_dados = df_dados.copy()
        self._dados_filtrados = pd.DataFrame()

    def remover_linhas_vazias(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove linhas vazias de um DataFrame.

        Args:
            df (DataFrame): DataFrame do qual as linhas vazias serão removidas.

        Returns:
            DataFrame: DataFrame sem linhas vazias.
        """
        return df.loc[df["Quantidade Induzida"].fillna(0) != 0]  # noqa: E712

    def filtrar_dados_por_data(self, data_inicial, data_final):
        """
        Método para filtrar dados por data.
        Retorna:
            DataFrame: Dados filtrados.
        """
        try:
            start = pd.to_datetime(data_inicial)
            end = pd.to_datetime(data_final)
        except Exception:
            self._dados_filtrados = pd.DataFrame()
            return

        # Garantir que a comparação use o mesmo tipo (Timestamp)
        self._dados_filtrados = self._df_dados.loc[
            self._df_dados["data_de_triagem"].between(start, end)
        ]
        return self

    def total_de_carga_induzida(self):
        """
        Método para calcular o total de carga induzida no intervalo informado.
        Retorna:
            int64: Total de carga induzida.
        """
        total = self._dados_filtrados["quantidade_induzida"].sum()
        print(
            f"Total de carga induzida calculado: {total}"
        )  # Debug: Exibir o total calculado
        cache.set("total_carga_induzida", total)  # Armazenar no cache
        return total

    def media_carga_induzida(self):
        """
        Método para calcular a média de carga induzida.
        Retorna:
            float: Média de carga induzida.
        """
        return self._dados_filtrados["quantidade_induzida"].mean()

    def rendimento_efetivo_hora(self):
        """
        Método para calcular o rendimento efetivo por hora.
        Retorna:
            float: Rendimento efetivo por hora.
        """
        return self._dados_filtrados["Rendimento Efetivo/h"].mean()

    def carga_induzida_por_centro(self):
        """Retorna a soma da `Quantidade Induzida` por `Centro de Tratamento`.

        Returns:
            pandas.Series: índice = Centro de Tratamento, valores = soma da
            carga.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            return pd.Series(dtype="int64")

        return self._dados_filtrados.groupby("Centro de Tratamento")[
            "Quantidade Induzida"
        ].sum()

    def rendimento_efetivo_por_centro(self):
        """Retorna a média de `Rendimento Efetivo/h` por `Centro de Tratamento`.

        Returns:
            Series: índice = Centro de Tratamento, valores = média do
            rendimento.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            return pd.Series(dtype="float64")

        return self._dados_filtrados.groupby("Centro de Tratamento")[
            "Rendimento Efetivo/h"
        ].mean()

    def carga_induzida_por_maquina(self):
        """Retorna um DataFrame com a soma da `Quantidade Induzida` por
        `Nº Máquina` e o respectivo `Centro de Tratamento`.

        Returns:
            DataFrame: índice = Nº Máquina, valores = soma da carga.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            return pd.DataFrame(
                columns=["Nº Máquina", "Quantidade Induzida", "Centro de Tratamento"]
            )

        return (
            self._dados_filtrados.groupby("Nº Máquina")
            .agg({"Quantidade Induzida": "sum", "Centro de Tratamento": "first"})
            .reset_index()
        )

    def rendimento_efetivo_por_maquina(self):
        """Retorna a média de `Rendimento Efetivo/h` por `Nº Máquina`.

        Returns:
            pandas.Series: índice = Nº Máquina, valores = média do rendimento.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            return pd.DataFrame(
                columns=["Nº Máquina", "Rendimento Efetivo/h", "Centro de Tratamento"]
            )

        return (
            self._dados_filtrados.groupby("Nº Máquina")
            .agg({"Rendimento Efetivo/h": "mean", "Centro de Tratamento": "first"})
            .reset_index()
        )

    @staticmethod
    def _adicionar_rotulo_maquina(df):
        """Adiciona uma coluna com rótulo formatado para máquinas.

        O rótulo segue o padrão: NºMáquina<br>IND - TIPO{sequência}
        onde IND são as 3 iniciais do Centro de Tratamento e a sequência
        reinicia para cada Centro de Tratamento.

        Args:
            df: DataFrame com colunas 'Nº Máquina' e 'Centro de Tratamento'

        Returns:
            DataFrame: com coluna adicional 'Rótulo Máquina'
        """
        df = df.copy().sort_values(by=["Centro de Tratamento", "Nº Máquina"])

        # Agrupar por centro e adicionar sequência dentro de cada grupo
        df["Sequência"] = df.groupby("Centro de Tratamento", sort=False).cumcount() + 1

        # Extrair as 3 primeiras letras do Centro de Tratamento
        df["Sigla Centro"] = df["Centro de Tratamento"].str[5:8].str.upper()

        # Criar o rótulo formatado
        df["Rótulo Máquina"] = (
            df["Nº Máquina"].astype(str)
            + "<br>"
            + df["Sigla Centro"].astype(str)
            + " - PBVS"
            + df["Sequência"].astype(str)
        )

        # Remover colunas auxiliares
        df.drop(columns=["Sequência", "Sigla Centro"])
        return df
