"""Classe para modelagem da carga induzida nas máquinas de triagem
automatizadas nos Centros de Tratamento.
"""

import pandas as pd

from src.models.base.auxiliares import Auxiliares


class CargaInduzidaModel:
    """
    Classe base para modelagem da carga induzida.
    Esta classe pode ser estendida para incluir atributos e métodos específicos
    relacionados à carga induzida nas máquinas de triagem nos centros de
    tratamento.
    """

    def __init__(self, path):
        self._linhas_desconsiderar = 8
        self._colunas_utilizar = {
            "Data de triagem": str,
            "Código MCU CTC": int,
            "Centro de Tratamento": str,
            "Nº Máquina": int,
            "Nome do Plano de Triagem": str,
            "Quantidade Induzida": int,
            "Rendimento Efetivo/h": int,
        }
        self._auxiliares = Auxiliares(
            str(path), self._linhas_desconsiderar, self._colunas_utilizar
        )
        self._dados = self._auxiliares.processar_dados()
        self._dados["Data de triagem"] = pd.to_datetime(
            self._dados["Data de triagem"], format="%d/%m/%Y"
        )
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
        self._dados_filtrados = self._dados.loc[
            self._dados["Data de triagem"].between(start, end)
        ]

    def total_de_carga_induzida(self):
        """
        Método para calcular o total de carga induzida no intervalo informado.
        Retorna:
            int64: Total de carga induzida.
        """
        return self._dados_filtrados["Quantidade Induzida"].sum()

    def media_carga_induzida(self):
        """
        Método para calcular a média de carga induzida.
        Retorna:
            float: Média de carga induzida.
        """
        return self._dados_filtrados["Quantidade Induzida"].mean()

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
            pandas.Series: índice = Centro de Tratamento, valores = soma da carga.
        """
        if self._dados_filtrados is None or self._dados_filtrados.empty:
            import pandas as pd

            return pd.Series(dtype="int64")

        return self._dados_filtrados.groupby("Centro de Tratamento")[
            "Quantidade Induzida"
        ].sum()

    def rendimento_efetivo_por_centro(self):
        """Retorna a média de `Rendimento Efetivo/h` por `Centro de Tratamento`.

        Returns:
            Series: índice = Centro de Tratamento, valores = média do rendimento.
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
