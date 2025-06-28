from datetime import datetime, timedelta

import streamlit as st


class Sidebar:
    """
        Classe para configuração da barra lateral do Streamlit.
    """
    PERIODOS_MAP = {
        "Último dia coletado": 0,
        "Essa Semana": 1,
        "Semana Passada": 2,
        "Esse Mês": 3,
        "Desde o mês Passado": 4,
        "Acumulado do Ano": 5
    }

    def __init__(self):
        self._tipo_maquina = None
        self._periodos = None

        # Defina o dicionário de mapeamento

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
        print(self._periodos)
        return self._periodos

    def configurar(self):
        # Configuração do tipo de máquina
        ontem = datetime.now() - timedelta(days=1)
        esta_semana = ontem - timedelta(days=datetime.now().weekday())
        # este_ano = ontem.year

        st.sidebar.radio(
            "Informe o tipo de máquina",
            ["Mensagens", "Encomendas"],
            key="tipo_maquina"
        )

        # Configuração do período
        st.sidebar.divider()
        # st.sidebar.title("Selecione o período")
        # st.sidebar.radio(
        #     "Selecione o período",
        #     ["Último dia coletado", "Essa Semana", "Semana Passada",
        #         "Esse Mês", "Desde o mês Passado", "Acumulado do Ano"],
        #     key="periodos"
        # )

        modo_data = st.sidebar.checkbox(
            "Selecionar Intervalo?",
            key="modo_data"
        )

        if modo_data:
            st.sidebar.date_input(
                "Intervalo",
                (esta_semana, ontem),
                # ontem, este_ano,
                format="DD/MM/YYYY",
                key="periodos"
            )
        else:
            st.sidebar.date_input(
                "Data",
                ontem, format="DD/MM/YYYY",
                key="periodos"
            )

    def get_periodo_mapeado(self):
        """
            Mapeia o período selecionado para um valor específico.
        """
        return st.session_state["periodos"]
        # return self.PERIODOS_MAP.get(periodo, None)
