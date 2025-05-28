"""Classe para apresentar o resumo da produtividade e eficiência das
    máquinas de triagem de cartas do CTCE.
"""
import streamlit as st
from streamlit_card import card

from data_processing import DataProcessing
from falhas_tecnicas import FalhasTecnicas


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
        self.carga_tratada.processar_carga_tratada()
        self.falhas_tecnicas.processar_dados()

        self._data = None
        self._set_dados()

    def _set_dados(self):
        """
            Define os dados a serem apresentados.
        """
        # carga_tratada_df = carga_tratada.recuperar_dados_pelo_centro(
        #     "CTCE Salvador")
        soma_carga_tratada = self.carga_tratada.get_soma_geral_de_carga_induzida(
            "16/08/2023")
        soma_falhas_tecnicas = self.falhas_tecnicas.get_soma_geral_de_falhas()

        self._data = soma_carga_tratada / \
            soma_falhas_tecnicas if soma_falhas_tecnicas != 0 else 0

    def _get_dados(self):
        """
            Retorna os dados a serem apresentados.
        """
        return self._data

    def definir_area_resumo(self):
        """
            Define a área de resumo para apresentação dos dados.
        """
        # self._set_dados()
        producao, eficiencia, disponibilidade, \
            media_local_por_falhas_tecnicas = st.columns(4)

        with producao:
            card(
                title=f"{self._get_dados():,.2f}",
                text="Média Geral de Objetos Alimentados por Falhas Técnicas \
                    nos Centros Avaliados" # ,
                # styles={
                #     "card": {
                #         "padding": "10px",
                #         "width": "50px",
                #         "height": "30px",
                #         "border-radius": "10px",
                #         "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                #     }
                # }
            )
        with eficiencia:
            card(
                title="Eficiência",
                text="Total de Objetos Alimentados"
                # styles={
                #     "card": {
                #         "width": "40px",
                #         "height": "33%",
                #         "border-radius": "60px",
                #         "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                #     }
                # }
            )
        with disponibilidade:
            card(
                title="Disponibilidade",
                text="Falhas Técnicas em Salvador"
                # styles={
                #     "card": {
                #         "width": "30px",
                #         "height": "33%",
                #         "border-radius": "60px",
                #         "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                #     }
                # }
            )

        with media_local_por_falhas_tecnicas:
            card(
                title="Média Local por Falhas Técnicas",
                text="Total de Objetos Alimentados"
                # styles={
                #     "card": {
                #         "width": "30px",
                #         "height": "33%",
                #         "border-radius": "60px",
                #         "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                #     }
                # }
            )


resumo = Resumo()
resumo.definir_area_resumo()
