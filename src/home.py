"""
    Classe para configuração da barra lateral do Streamlit.
"""
import streamlit as st

# from pages.resumo import Resumo
from sidebar_config import Sidebar


class App:
    def _definir_config_app(self):
        """
            Define a configuração do aplicativo.
        """
        st.set_page_config(
            page_title="Relatório de Manutenção",
            page_icon=":bar_chart:",
            layout="wide",
            menu_items={
                'Get Help': "https://www.extrema.com.br",
                'Report a bug': "mailto:domingos_alcantara@yahoo.com.br"}
        )

    def _definir_paginas(self):
        """
            Define as páginas do aplicativo.
        """

        resumo = st.Page("pages/resumo.py", title="Resumo")
        atolamentos = st.Page("pages/atolamentos.py",
                              title="Atolamentos e Falhas Técnicas")
        monitoramento = st.Page("pages/monitoramento.py", title="Monitoramento")
        analise_operacional = st.Page(
            "pages/analise_operacional.py", title="Análise Operacional")
        comparativo = st.Page("pages/comparativo.py", title="Comparativo")

        pg = st.navigation([resumo, atolamentos, monitoramento,
                            analise_operacional, comparativo])
        pg.run()

    def main(self):
        """
            Função principal para executar o Streamlit.
        """
        self._definir_config_app()

        # Configuração da barra lateral
        sidebar = Sidebar()
        sidebar.configurar()

        # Definindo as páginas
        self._definir_paginas()


if __name__ == "__main__":
    app = App()
    app.main()
