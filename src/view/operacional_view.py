import streamlit as st


class OperacionalView:
    """Classe para visualização dos dados operacionais."""

    def __init__(self):
        """Inicializa a classe com o modelo de dados operacionais."""
        # self._model = model

    def exibir_centros(self, centros):
        """Exibe os dados operacionais na interface do Streamlit."""
        # st.title("Dados Operacionais")

        if not centros:
            st.warning("Nenhum dado operacional encontrado.")
            return
        else:
            centros_selecionados = st.sidebar.multiselect(
                "Centros de Tratamento",
                centros, centros
            )

        if centros_selecionados:
            st.session_state["centros_selecionados"] = centros_selecionados

    def exibir_maquinas(self, maquinas):
        """Exibe as máquinas de triagem na interface do Streamlit."""
        if not maquinas:
            st.warning("Nenhuma máquina de triagem encontrada.")
            return
        else:
            st.sidebar.multiselect(
                "Máquinas de Triagem",
                maquinas, maquinas
            )
