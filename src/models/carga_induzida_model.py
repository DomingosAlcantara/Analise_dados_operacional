"""Classe para modelagem da carga induzida nas máquinas de triagem
automatizadas nos Centros de Tratamento.
"""

import pandas as pd

# from src.utils.cache import cache


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
        mascara = self._df_dados["data_de_triagem"].between(start, end)

        self._dados_filtrados = self._df_dados.loc[mascara].copy()
        print(
            f"Dados apos filtragem: {len(self._dados_filtrados)} registros"
        )  # Debug: Exibir número de registros antes
        return self

    def total_de_carga_induzida(self):
        """
        Método para calcular o total de carga induzida no intervalo informado.
        Retorna:
            int64: Total de carga induzida.
        """
        return int(self._dados_filtrados["quantidade_induzida"].sum())
        # print(
        #     f"Total de carga induzida calculado: {total}"
        # )  # Debug: Exibir o total calculado
        # # cache.set("total_carga_induzida", total)  # Armazenar no cache
        # return total

    def obter_media_diaria(self):
        """
        Método para calcular a média diária de carga induzida.
        Retorna:
            float: Média diária de carga induzida.
        """
        self._dados_filtrados["dia exato"] = self._dados_filtrados[
            "data_de_triagem"
        ].dt.date

        print(
            f"Dados apos agrupamento por dia: {len(self._dados_filtrados['dia exato'].unique())} dias"
        )
        return (
            self._dados_filtrados.groupby("dia exato")["quantidade_induzida"]
            .sum()
            .mean()
        )

    def media_carga_induzida(self):
        """
        Método para calcular a média de carga induzida.
        Retorna:
            float: Média de carga induzida.
        """
        return self._dados_filtrados["quantidade_induzida"].mean()

    def rendimento_efetivo_medio(self) -> float:
        """
        Método para calcular o rendimento efetivo por hora.
        Retorna:
            float: Rendimento efetivo por hora.
        """
        return self._dados_filtrados["rendimento_efetivo/h"].mean()

    def carga_induzida_por_centro(self):
        """Retorna a soma da `Quantidade Induzida` por `Centro de Tratamento`.

        Returns:
            pandas.Series: índice = Centro de Tratamento, valores = soma da
            carga.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            return pd.Series(dtype="int64")

        return self._dados_filtrados.groupby("centro_de_tratamento")[
            "quantidade_induzida"
        ].sum()

    def rendimento_efetivo_por_centro(self):
        """Retorna a média de `Rendimento Efetivo/h` por `Centro de Tratamento`.

        Returns:
            Series: índice = Centro de Tratamento, valores = média do
            rendimento.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            return pd.Series(dtype="float64")

        return self._dados_filtrados.groupby("centro_de_tratamento")[
            "rendimento_efetivo/h"
        ].mean()

    def carga_induzida_por_maquina(self):
        """Retorna um DataFrame com a soma da `Quantidade Induzida` por
        `Nº Máquina` e o respectivo `Centro de Tratamento`.

        Returns:
            DataFrame: índice = Nº Máquina, valores = soma da carga.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            return pd.DataFrame(
                columns=["nº_máquina", "quantidade_induzida", "centro_de_tratamento"]
            )

        return (
            self._dados_filtrados.groupby("nº_máquina")
            .agg({"quantidade_induzida": "sum", "centro_de_tratamento": "first"})
            .reset_index()
        )

    def rendimento_efetivo_por_maquina(self):
        """Retorna a média de `Rendimento Efetivo/h` por `Nº Máquina`.

        Returns:
            pandas.Series: índice = Nº Máquina, valores = média do rendimento.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            return pd.DataFrame(
                columns=["nº_máquina", "rendimento_efetivo/h", "centro_de_tratamento"]
            )

        return (
            self._dados_filtrados.groupby("nº_máquina")
            .agg({"rendimento_efetivo/h": "mean", "centro_de_tratamento": "first"})
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
        df = df.copy().sort_values(by=["centro_de_tratamento", "nº_máquina"])

        # Agrupar por centro e adicionar sequência dentro de cada grupo
        df["Sequência"] = df.groupby("centro_de_tratamento", sort=False).cumcount() + 1

        # Extrair as 3 primeiras letras do Centro de Tratamento
        df["Sigla Centro"] = df["centro_de_tratamento"].str[5:8].str.upper()

        # Criar o rótulo formatado
        df["Rótulo Máquina"] = (
            df["nº_máquina"].astype(str)
            + "<br>"
            + df["Sigla Centro"].astype(str)
            + " - PBVS"
            + df["Sequência"].astype(str)
        )

        # Remover colunas auxiliares
        df.drop(columns=["Sequência", "Sigla Centro"])
        return df
