""" Classe para vizualizar os dados de atolamento de cartas do CTCE.
    """
import streamlit as st
from streamlit_card import card


class Atolamentos:
    """
        Classe para vizualizar os dados de atolamento de cartas do CTCE.
    """

    def __init__(self, data):
        """
            Inicializa a classe Atolamentos com os dados fornecidos.
        """
        self.data = data
        self._set_dados()

    def _set_dados(self):
        """
            Define os dados a serem apresentados.
        """
        # Aqui você deve carregar os dados reais de atolamento
        self.atolamentos = 1

    def mostrar_atolamentos(self):
        """
            Mostra os dados de atolamento na interface do Streamlit.
        """
        st.title("Atolamentos de Cartas")
        card(
            title="Atolamentos",
            text="Visualização dos dados de atolamento de cartas do CTCE.",
            # content=f"Total de atolamentos: {len(self.atolamentos)}"
        )
        st.write(self.atolamentos)
        if self.atolamentos > 0:
            st.dataframe(self.atolamentos)
        else:
            st.write("Nenhum atolamento registrado.")


# Inicializando a classe Atolamentos com dados fictícios
atolamentos = Atolamentos(data=st.session_state.get("data", None))
# Exibindo os atolamentos
atolamentos.mostrar_atolamentos()
