""" Classe para vizualizar os dados de atolamento de cartas do CTCE.
    """
import streamlit as st
from streamlit_card import card


class ParadasView:
    """
        Classe para vizualizar os dados de atolamento de cartas do CTCE.
    """

    def mostrar_atolamentos(self, atolamentos):
        """
            Mostra os dados de atolamento na interface do Streamlit.
        """
        st.title("Atolamentos de Cartas")
        card(
            title="Atolamentos",
            text="Visualização dos dados de atolamento de cartas do CTCE.",
            # content=f"Total de atolamentos: {len(self.atolamentos)}"
        )
        st.write(atolamentos)
        if len(atolamentos) > 0:
            st.dataframe(atolamentos)
        else:
            st.write("Nenhum atolamento registrado.")

    def mostrar_maquinas(self, maquinas):
        """
            Mostra as máquinas existentes no Centro de Tratamento.
        """
        st.title("Máquinas do Centro de Tratamento")
        card(
            title="Máquinas",
            text="Visualização das máquinas existentes no Centro de\
                  Tratamento.",
        )
        if maquinas:
            st.write(maquinas)
            st.dataframe(maquinas)
        else:
            st.write("Nenhuma máquina registrada.")


# Inicializando a classe Atolamentos com dados fictícios
atolamentos = ParadasView()
# Exibindo os atolamentos
# atolamentos.mostrar_atolamentos()
