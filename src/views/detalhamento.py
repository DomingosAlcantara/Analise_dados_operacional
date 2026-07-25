"""Classe para exibição das opções de detalhamento das métricas"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from src.controllers.detalhamento import Detalhamento as DetalhamentoController

dash.register_page(__name__, path="/detalhamento", name="Detalhamento")


class Detalhamento:
    def obter_layout(self) -> dbc.Container:
        """
        Retorna o layout da página de detalhamento.

        Returns:
            dbc.Container: Layout da página.
        """

        return dbc.Container(
            [
                html.H3(
                    "Detalhamento Operacional",
                    className="mt-4 mb-4 text-primary text-center",
                ),
                # Nível 1 - Centro vs Máquinas
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Visão Geral:",
                                    className="fw-bold d-block mb-1 text-center",
                                ),
                                dbc.RadioItems(
                                    id="detalhamento-nivel-1",
                                    options=[
                                        {
                                            "label": "Centro de Tratamento",
                                            "value": "centro",
                                        },
                                        {"label": "Máquinas", "value": "maquinas"},
                                    ],
                                    value="centro",
                                    inline=True,
                                    className="btn-group",
                                    inputClassName="btn-check",
                                    labelClassName="btn btn-outline-primary",
                                    labelCheckedClassName="active",
                                ),
                            ],
                            width="auto",
                        ),
                    ],
                    className="mb-3 justify-content-center",
                ),
                # Nível 2 - Sub-opções dinâmicas
                dbc.Row(
                    [dbc.Col(id="detalhamento-container-nivel-2", width="auto")],
                    className="mb-3 justify-content-center",
                ),
                # Nível 3 - Métricas da Máquina
                dbc.Row(
                    [dbc.Col(id="detalhamento-container-nivel-3", width="auto")],
                    className="mb-4 justify-content-center",
                ),
                html.Hr(),
                # Área de Gráficos e Tabelas
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="detalhamento-grafico-principal"),
                            ],
                            width=12,
                        ),
                    ]
                ),
            ],
            fluid=True,
        )


controller = DetalhamentoController()
controller.registrar_callbacks()

view = Detalhamento()


def get_layout():
    return view.obter_layout()


layout = get_layout
