import streamlit as st


class Sidebar:
    """
        Classe para configuração da barra lateral do Streamlit.
    """

    def __init__(self):
        self._tipo_maquina = None
        self._periodos = None

    def set_maquina(self, tipo_maquina):
        """
            Configura o tipo de máquina.
        """
        self._tipo_maquina = tipo_maquina

    def set_periodos(self, periodos):
        """
            Configura o período.
        """
        self._periodos = periodos

    def get_maquina(self):
        """
            Retorna o tipo de máquina.
        """
        return self._tipo_maquina

    def get_periodos(self):
        """
            Retorna o período.
        """
        return self._periodos

    def configurar(self):
        # Configuração do tipo de máquina
        st.sidebar.title("Selecione o tipo de máquina")
        tipo_maquina = st.sidebar.radio(
            "Informe o tipo de máquina",
            ["Mensagens", "Encomendas"],
            key="tipo_maquina"
        )

        # Configuração do período
        st.sidebar.divider()
        st.sidebar.title("Selecione o período")
        periodos = st.sidebar.radio(
            "Selecione o período",
            ["Último dia coletado", "Essa Semana", "Semana Passada",
                "Esse Mês", "Desde o mês Passado", "Acumulado do Ano"],
            key="periodos"
        )

        # Armazenar no session_state
        self.set_maquina(tipo_maquina)
        self.set_periodos(periodos)
