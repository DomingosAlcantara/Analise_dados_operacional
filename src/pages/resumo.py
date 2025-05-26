"""Classe para apresentar o resumo da produtividade e eficiência das
    máquinas de triagem de cartas do CTCE.
"""
import streamlit as st
from streamlit_card import card


class Resumo:
    """
        Classe para apresentar o resumo da produtividade e eficiência das
        máquinas de triagem de cartas do CTCE.
    """

    def __init__(self, data):
        """
            Inicializa a classe Resumo com os dados fornecidos.
        """
        self._data = data

    def _set_dados(self, dados):
        """
            Define os dados a serem apresentados.
        """
        self._data = dados

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
                title="Produção",
                text="Média Geral de Objetos Alimentados por Falhas Técnicas \
                    nos Centros Avaliados"  # ,
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


resumo = Resumo(data=None)
resumo.definir_area_resumo()
