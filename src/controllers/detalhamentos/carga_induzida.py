"""
Controller resposável pelas lógicas e injeção de dados da View Carga Induzida.
"""

import plotly.graph_objects as go
from dash import Input, Output, callback, no_update

from src.engine import empresa
from src.views.detalhamentos.carga_induzida import CargaInduzida


class CargaInduzidaController:
    def __init__(self):
        self._empresa = empresa

    def registrar_callbacks(self):
        @callback(
            [
                Output(CargaInduzida().ID_GRAFICO_CARGA_TURNO, "figure"),
                Output(CargaInduzida().ID_GRAFICO_RENDIMENTO_TURNO, "figure"),
                Output(CargaInduzida().ID_TEMPO_TURNO1, "children"),
                Output(CargaInduzida().ID_TEMPO_TURNO2, "children"),
                # Output(CargaInduzida().ID_TEMPO_TURNO3, "children"),
                Output(CargaInduzida().ID_GRAFICO_CARGA_HORA, "figure"),
            ],
            [
                Input("detalhamento-nivel-1", "value"),
                Input("detalhamento-selecao-maquina", "value"),
            ],
            prevent_initial_call=True,
        )
        def _atualizar_metricas_maquina(nivel1, maquina_selecionada):
            """Busca os dados no Model, e injeta nos gráficos

            Args:
                nivel1 (_type_): _description_
                maquina_selecionada (_type_): _description_
            """

            # Se não estiver na visão de máquina, aborta a atualização
            if nivel1 != "maquina":
                return no_update, no_update, no_update, no_update, no_update, no_update

            # Mock dos dados (Aqui entra a requisição ao self._empresa)
            carga_turno = [1, 2, 3, 4]
            rendimento_turno = [1, 2, 3, 4]
            tempo_turno1 = "02:38:00"
            tempo_turno2 = "02:54:00"
            # tempo_turno3 = "03:10:00"
            carga_hora = [1, 2, 3, 4]

            fig_carga_turno = go.Figure(
                data=[
                    go.Bar(
                        name="T1",
                        x=["Turno 1", "Turno 2", "Turno 3"],
                        y=carga_turno,
                        marker_color="#3498db",
                    ),
                    go.Bar(
                        name="T2",
                        x=["Turno 1", "Turno 2", "Turno 3"],
                        y=rendimento_turno,
                        marker_color="#2ecc71",
                    ),
                ]
            )

            fig_carga_turno.update_layout(
                title="Carga Induzida", margin=dict(l=20, r=20, t=40, b=20)
            )

            fig_rendimento = go.Figure(
                data=[
                    go.Bar(
                        name="T1", x=["Rendimento"], y=[2200], marker_color="#9b59b6"
                    ),
                    go.Bar(
                        name="T2", x=["Rendimento"], y=[2500], marker_color="#e67e22"
                    ),
                ]
            )
            fig_rendimento.update_layout(
                title="Rend. Efetivo/h", margin=dict(l=20, r=20, t=40, b=20)
            )

            fig_carga_hora = go.Figure(
                data=[
                    go.Scatter(
                        x=["08:00", "09:00", "10:00", "11:00", "12:00"],
                        y=[2000, 2500, 2100, 2800, 1500],
                        mode="lines+markers",
                        line=dict(color="#e74c3c", width=3),
                    )
                ]
            )
            fig_carga_hora.update_layout(
                title="Carga Triada por Hora", margin=dict(l=20, r=20, t=40, b=20)
            )

            return (
                fig_carga_turno,
                fig_rendimento,
                tempo_turno1,
                tempo_turno2,
                # tempo_turno3,
                fig_carga_hora,
            )
