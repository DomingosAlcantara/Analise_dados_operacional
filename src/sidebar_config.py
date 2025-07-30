from datetime import datetime, timedelta

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
        print(self._periodos)
        return self._periodos

    def _definir_maquina_em_analise(self):
        """
            Define o tipo de máquina em análise.
        """
        return st.sidebar.radio(
            "Selecione o tipo de máquina",
            ["Mensagens", "Encomendas"],
            key="tipo_maquina"
        )

    def _is_interval(self):
        """
            Verifica se o modo de intervalo está selecionado.
        """
        return st.sidebar.checkbox(
            "Selecionar Intervalo?",
            key="modo_data"
        )

    def configurar(self):
        # Configuração do tipo de máquina
        ontem = (datetime.now() - timedelta(days=1)).date()
        esta_semana = (ontem - timedelta(days=datetime.now().weekday()))
        self._definir_maquina_em_analise()

        st.sidebar.divider()

        intervalo = self._is_interval()
        label = "Intervalo" if intervalo else "Data"
        default_value = (esta_semana, ontem) if intervalo else ontem

        st.sidebar.date_input(
            label,
            default_value,
            format="DD/MM/YYYY",
            key="periodos"
        )

        # if self._is_interval():
        #     st.sidebar.date_input(
        #         "Intervalo",
        #         (esta_semana, ontem),
        #         format="DD/MM/YYYY",
        #         key="periodos"
        #     )
        # else:
        #     st.sidebar.date_input(
        #         "Data",
        #         ontem, format="DD/MM/YYYY",
        #         key="periodos"
        #     )

    def get_periodo_mapeado(self):
        """
            Mapeia o período selecionado para um valor específico.
        """
        return st.session_state["periodos"]
