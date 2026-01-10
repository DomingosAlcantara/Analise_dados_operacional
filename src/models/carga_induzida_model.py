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
        Método para calcular o total de carga induzida.
        Retorna:
            int: Total de carga induzida.
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
