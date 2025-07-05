"""Classe para apresentar o resumo da produtividade e eficiência das
    máquinas de triagem de cartas do CTCE.
"""
import streamlit as st
from streamlit_card import card

from data_processing import DataProcessing
from falhas_tecnicas import FalhasTecnicas
from sidebar_config import Sidebar

# from src.pages.cartao import card


class Resumo:
    """
        Classe para apresentar o resumo da produtividade e eficiência das
        máquinas de triagem de cartas do CTCE.
    """

    def __init__(self):
        """
            Inicializa a classe Resumo com os dados fornecidos.
        """
        self.path_carga_tratada = \
            "/home/domingos/Documentos/Dados/Carga Tratada/"
        self.path_falhas_tecnicas = "/home/domingos/Documentos/Dados/Técnica/"
        self.carga_tratada = DataProcessing(self.path_carga_tratada)
        self.falhas_tecnicas = FalhasTecnicas(self.path_falhas_tecnicas)
        self.sidebar = Sidebar()
        self.carga_tratada.processar_carga_tratada()
        self.falhas_tecnicas.processar_dados()
        self.tipo_maquina = st.session_state.get("tipo_maquina", "Mensagens")
        self._periodos = self.sidebar.get_periodo_mapeado()
        self.soma_local_falhas = None
        self._falhas_periodo = 0
        self._data = None
        self._set_dados()

    def _set_dados(self):
        """
            Define os dados a serem apresentados.
        """
        soma_carga_tratada = self.carga_tratada. \
            get_soma_geral_de_carga_induzida(self._periodos)
        soma_falhas_tecnicas = self.falhas_tecnicas.get_soma_geral_de_falhas(
            self._periodos)
        self.soma_local_falhas = self.falhas_tecnicas. \
            get_soma_falhas_tecnicas()
        self._falhas_periodo = self.soma_local_falhas(self._periodos)

        self._data = soma_carga_tratada / \
            soma_falhas_tecnicas if soma_falhas_tecnicas != 0 else 0

    def _media_local_por_falhas_tecnicas(self):
        """
            Calcula a média local por falhas técnicas.
        """
        if self._falhas_periodo > 0:
            return self.carga_tratada.get_soma_carga_induzida_por_centro(
                self._periodos) / self._falhas_periodo
        else:
            return 0

    def _get_dados(self):
        """
            Retorna os dados a serem apresentados.
        """
        return self._data

    def _formatar_valores(self, valor):
        """
            Formata os valores para exibição.
        """
        return f"{valor:,.0f}".replace(",", "X"). \
            replace(".", ",").replace("X", ".")

    def definir_area_resumo(self):
        """
            Define a área de resumo para apresentação dos dados.
        """
        # clicado = False
        nome_cartoes = ["producao", "eficiencia", "disponibilidade",
                        "Média Local por Falhas Técnicas"]

        # Estado para armazenar o cartão selecionado
        if "cartao_selecionado" not in st.session_state:
            st.session_state["cartao_selecionado"] = None
        if "click_count" not in st.session_state:
            st.session_state.click_count = 0

        def selecionar_cartao(index):
            """
                Função para selecionar um cartão.
            """
            st.session_state.cartao_selecionado = index
            st.session_state.click_count += 1

        colunas = st.columns(len(nome_cartoes))

        # Dados para cada cartão
        dados_cartoes = [
            {
                "titulo": self._formatar_valores(self._get_dados()),
                "texto": "Média Geral de Objetos Alimentados por Falhas \
                    Técnicas nos Centros Avaliados",
                "cor": "#4CAF50"
            },
            {
                "titulo": self._formatar_valores(
                    self.carga_tratada.get_soma_carga_induzida_por_centro(
                        self._periodos)),
                "texto": "Total de Objetos Alimentados neste Centro",
                "cor": "#2196F3"
            },
            {
                "titulo": self._formatar_valores(self._falhas_periodo),
                "texto": "Falhas Técnicas em Salvador",
                "cor": "#FF9800"
            },
            {
                "titulo": self._formatar_valores(
                    self._media_local_por_falhas_tecnicas()),
                "texto": "Média de Objetos por Falhas Técnicas em Salvador",
                "cor": "#9C27B0"
            }
        ]

        for i, col in enumerate(colunas):
            with col:
                card(
                    title=dados_cartoes[i]["titulo"],
                    text=dados_cartoes[i]["texto"],
                    key=nome_cartoes[i],
                    on_click=lambda x=i: selecionar_cartao(x),
                    styles={
                        "card": {
                            "border": "4px solid #FFD700"
                            if st.session_state.cartao_selecionado == i
                            else "",
                            "box-shadow": "0 0 10px #FFD700"
                            if st.session_state.cartao_selecionado == i
                            else "",
                            "cursor": "pointer"
                        },
                        "title": {
                            "color": dados_cartoes[i]["cor"],
                            "fontSize": "80px",
                            "fontWeight": "bold"
                        },
                    }
                )

                # if clicado:  # and st.session_state.cartao_selecionado != i:
                #     st.session_state["cartao_selecionado"] = i
                #     st.session_state.click_count += 1
                #     i = 0

        if st.session_state.cartao_selecionado is not None:
            st.success(
                f"Você selecionou o cartão: \
                    {nome_cartoes[st.session_state.cartao_selecionado]}\
                        (Total de cliques: {st.session_state.click_count})"
            )


resumo = Resumo()
resumo.definir_area_resumo()
