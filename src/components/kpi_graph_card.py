from dash import dcc, html


class KpiGraphCard:
    """Componente para mostrar um gráfico dentro de um card de KPI.

    Args:
        label (str): Texto do rótulo do gráfico.
        figure (plotly.graph_objs._figure.Figure | dict): Figura do gráfico.
        graph_id (str, optional): ID do componente Graph. Default None.
        extra_class (str, optional): Classes CSS adicionais. Default ''
    """

    def __init__(self, figure=None, graph_id=None, extra_class=""):
        # self.label = label
        self.figure = figure or {}
        self.graph_id = graph_id
        self.extra_class = extra_class

    def display(self):
        full_class_name = f"kpi-block {self.extra_class}".strip()

        graph_props = {}
        if self.graph_id:
            graph_props["id"] = self.graph_id

        return html.Div(
            [
                dcc.Graph(
                    figure=self.figure,
                    **graph_props,
                    className="kpi-graph",
                    config={"displayModeBar": False, "responsive": True},
                    style={"height": "100%", "width": "100%"},
                ),
            ],
            className=full_class_name,
        )
