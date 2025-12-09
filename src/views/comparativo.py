"""Classe para apresentar o comparativo entre Centros de Tratamento"""

import dash
from dash import Input, Output, dcc, html

dash.register_page(__name__, path="/comparativo", name="Comparativo")


class Comparativo:
    def __init__(self, app_instance):
        self.app = app_instance
        self.dropdown_id = "comparativo-dropdown"
        self.graph_id = "comparativo-graph"
        self.register_callbacks()

    def layout(self):
        return html.Div(
            [
                html.H1(
                    "Comparativo entre Centros de Tratamento", className="page-title"
                ),
                html.Div("Selecione um parâmetro para comparar:"),
                dcc.Dropdown(
                    id=self.dropdown_id,
                    options=[
                        {"label": "Parâmetro 1", "value": "param1"},
                        {"label": "Parâmetro 2", "value": "param2"},
                    ],
                    value="param1",
                    clearable=False,
                    style={"width": "50%"},
                ),
                dcc.Graph(id=self.graph_id),
            ]
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

    comparativo_page_instance = Comparativo(app)
    return comparativo_page_instance.layout()


layout = get_layout
