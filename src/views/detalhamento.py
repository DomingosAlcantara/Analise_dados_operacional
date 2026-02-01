"""Classe para apresentar o comparativo entre Centros de Tratamento"""

import dash
from dash import Input, Output, html

from src.components.kpi_card import KpiCard

dash.register_page(__name__, path="/detalhamento", name="Detalhamento")


class Detalhamento:
    def __init__(self, app_instance, register_callbacks=True):
        self.app = app_instance
        self.dropdown_id = "comparativo-dropdown"
        self.graph_id = "comparativo-graph"
        if register_callbacks:
            self.register_callbacks()

    def layout(self):
        carga_induzida_centro = KpiCard(
            "Carga Induzida Média por Centro",
            value="75%",
            card_id="kpi-carga-induzida-centro",
        )

        media_carga_centro_dia = KpiCard(
            "Média de Carga Induzida / Dia",
            value="60%",
            card_id="kpi-media-carga-centro-dia",
        )

        rendimento_centro_hora = KpiCard(
            "Rendimento Efetivo / h",
            value="85%",
            card_id="kpi-rendimento-centro-hora",
        )

        graph_carga_induzida_turno = KpiCard(
            "Gráfico de Carga Induzida por Turno",
            value="",
            card_id="kpi-graph-carga-induzida-turno",
        )

        graph_rendimento_efetivo_turno = KpiCard(
            "Gráfico de Rendimento Efetivo por Turno",
            value="",
            card_id="kpi-graph-rendimento-efetivo-turno",
        )

        return html.Div(
            [
                html.Div(
                    [
                        carga_induzida_centro.display(),
                        media_carga_centro_dia.display(),
                        rendimento_centro_hora.display(),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "height": "84vh",
                        "width": "100%",
                        "flex": "1",
                        "gap": "0px",
                    },
                ),
                html.Div(
                    [
                        graph_carga_induzida_turno.display(),
                        graph_rendimento_efetivo_turno.display(),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "height": "84vh",
                        "width": "100%",
                        "flex": "1.5",
                        "gap": "0px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
                "height": "84vh",
                "width": "100%",
                "gap": "0px",
            },
            className="kpi-table",
        )

    def register_callbacks(self):
        @self.app.callback(
            Output(self.graph_id, "figure"),
            Input(self.dropdown_id, "value"),
        )
        def update_graph(selected_param):
            # Lógica para atualizar o gráfico com base no parâmetro selecionado
            import plotly.express as px

            df = px.data.gapminder().query("year == 2007")
            fig = px.bar(
                df,
                x="continent",
                y="pop",
                color="continent",
                title=f"Comparativo baseado em {selected_param}",
            )
            return fig


def get_layout():
    from src.app import app

    return Detalhamento(app, register_callbacks=False).layout()


layout = get_layout
