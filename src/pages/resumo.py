"""Classe para apresentar o resumo da produtividade e eficiência das
    máquinas de triagem de cartas do CTCE.
"""
import streamlit as st
from streamlit_card import card

from src.data_processing import DataProcessing
from src.falhas_tecnicas import FalhasTecnicas
from src.sidebar_config import Sidebar


class Resumo:
    """
        Classe para apresentar o resumo da produtividade e eficiência das
        máquinas de triagem de cartas do CTCE.
    """

    def __init__(self):
        """
            Inicializa a classe Resumo com os dados fornecidos.
        """
        self.path_carga_tratada = "C:/Users/80891950/Downloads/Relatório Pitney Bower/Dados/Carga Tratada/"
        self.path_falhas_tecnicas = "C:/Users/80891950/Downloads/Relatório Pitney Bower/Dados/Técnica/"
        self.carga_tratada = DataProcessing(self.path_carga_tratada)
        self.falhas_tecnicas = FalhasTecnicas(self.path_falhas_tecnicas)
        self.sidebar = Sidebar()
        self.carga_tratada.processar_carga_tratada()
        self.falhas_tecnicas.processar_dados()
        self.tipo_maquina = st.session_state.get("tipo_maquina", "Mensagens")
        self._periodos = self.sidebar.get_periodo_mapeado()
        self.soma_local_falhas = None
        self.falhas_periodo = 0

        # self._data_pesquisa = "15/08/2023"

        self._data = None
        self._set_dados()

    def _set_dados(self):
        """
            Define os dados a serem apresentados.
        """
        soma_carga_tratada = self.carga_tratada.\
            get_soma_geral_de_carga_induzida(self._periodos)
        soma_falhas_tecnicas = self.falhas_tecnicas.\
            get_soma_geral_de_falhas(self._periodos)
        self.soma_local_falhas = self.falhas_tecnicas.\
            get_soma_falhas_tecnicas()
        self.falhas_periodo = self.soma_local_falhas(self._periodos)

        self._data = soma_carga_tratada / \
            soma_falhas_tecnicas if soma_falhas_tecnicas != 0 else 0

    def _media_local_por_falhas_tecnicas(self):
        """
            Calcula a média local por falhas técnicas.
        """
        if self.falhas_periodo > 0:
            return self.carga_tratada.get_soma_carga_induzida_por_centro(
                self._periodos) / self.falhas_periodo
        else:
            return 0

    def _get_dados(self):
        """
            Retorna os dados a serem apresentados.
        """
        return self._data

    def definir_area_resumo(self):
        """
            Define a área de resumo para apresentação dos dados.
        """
        producao, eficiencia, disponibilidade, \
            media_local_por_falhas_tecnicas = st.columns(4)

        with producao:
            card(
                title=f"{self._get_dados():,.0f}".replace(
                    ",", "X").replace(".", ",").replace("X", "."),
                text="Média Geral de Objetos Alimentados por Falhas Técnicas \
                    nos Centros Avaliados",
                on_click=lambda: print("Card de Produção clicado!"),
                styles={
                    "card": {},
                    "title": {
                        "font-size": "90px",
                        "font-weight": "bold",
                        "color": "#4CAF50"
                    },
                }
            )
        with eficiencia:
            card(
                title=f"{self.carga_tratada.get_soma_carga_induzida_por_centro(
                    self._periodos):,.0f}".replace(
                    ",", "X").replace(".", ",").replace("X", "."),
                text="Total de Objetos Alimentados neste Centro",
                styles={
                    "card": {},
                    "title": {
                        "font-size": "80px",
                        "font-weight": "bold",
                        "color": "#2196F3"
                    },
                }
            )
        with disponibilidade:
            card(
                title=f"{self.falhas_periodo:,.0f}".replace(
                    ",", "X").replace(".", ",").replace("X", "."),
                text="Falhas Técnicas em Salvador",
                styles={
                    "card": {},
                    "title": {
                        "font-size": "80px",
                        "font-weight": "bold",
                        "color": "#FF9800"
                    },
                }
            )

        with media_local_por_falhas_tecnicas:
            card(
                title=f"{self._media_local_por_falhas_tecnicas():,.0f}".
                replace(",", "X").replace(".", ",").replace("X", "."),
                text="Média de Objetos por Falhas Técnicas em Salvador",
                styles={
                    "card": {},
                    "title": {
                        "font-size": "80px",
                        "font-weight": "bold",
                        "color": "#9C27B0"
                    },
                }
            )


resumo = Resumo()
resumo.definir_area_resumo()
