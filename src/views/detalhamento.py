"""Classe para exibição das opções de detalhamento das métricas"""

import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path="/detalhamento", name="Detalhamento")


class Detalhamento:
    def obter_layout(self) -> dbc.Container:
        """
        Retorna o layout da página de detalhamento.

        Returns:
            dbc.Container: Layout da página.
        """

        opcoes_maquinas = [
            {"label": f"PBVS {i}", "value": f"PBVS {i}"}
            for i in range(
                1, 4
            )  # Ou dinâmico via self.empresa_model] #self._empresa_model.listar_maquinas()
        ]
        opcoes_metricas = [
            {"label": "Carga Induzida", "value": "carga"},
            {"label": "Atolamentos", "value": "atolamentos"},
            {"label": "Falhas Técnicas", "value": "falhas_tecnicas"},
            {"label": "Rejeitos", "value": "rejeitos"},
        ]

        return dbc.Container(
            [
                dbc.Collapse(
                    html.Div(
                        [
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
                                                    {
                                                        "label": "Máquinas",
                                                        "value": "maquinas",
                                                    },
                                                ],
                                                value="centro",
                                                inline=True,
                                                className="btn-group btn-group-lg",
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
                            # Nível 2 - Métricas do Centro (Inicia visivel)
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Métricas do Centro:",
                                                className="fw-bold d-block mb-1 text-center",
                                            ),
                                            dbc.RadioItems(
                                                id="detalhamento-metricas-centro",
                                                options=opcoes_metricas,
                                                value="carga",
                                                inline=True,
                                                className="btn-group btn-group-lg",
                                                inputClassName="btn-check",
                                                labelClassName="btn btn-outline-secondary",
                                                labelCheckedClassName="active",
                                            ),
                                        ],
                                        width="auto",
                                    )
                                ],
                                id="container-metricas-centro",
                                className="mb-3 justify-content-center",
                                style={"display": "flex"},  # Inicialmente visível
                            ),
                            # Nível 2 - Seleção de Máquina (Inicia escondido)
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Selecione a Máquina:",
                                                className="fw-bold d-block mb-1 text-center",
                                            ),
                                            dbc.RadioItems(
                                                id="detalhamento-selecao-maquina",
                                                options=opcoes_maquinas,
                                                value=(
                                                    opcoes_maquinas[0]["value"]
                                                    if opcoes_maquinas
                                                    else None
                                                ),
                                                inline=True,
                                                className="btn-group btn-group-lg",
                                                inputClassName="btn-check",
                                                labelClassName="btn btn-outline-info",
                                                labelCheckedClassName="active",
                                            ),
                                        ],
                                        width="auto",
                                    )
                                ],
                                id="container-selecao-maquina",
                                className="mb-3 justify-content-center",
                                style={"display": "none"},  # Inicialmente escondido
                            ),
                            # Nível 3 - Métricas da Máquina (Inicia escondido)
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Métricas da Máquina:",
                                                className="fw-bold d-block mb-1 text-center",
                                            ),
                                            dbc.RadioItems(
                                                id="detalhamento-metricas-maquinas",
                                                options=opcoes_metricas,
                                                value="carga",
                                                inline=True,
                                                className="btn-group btn-group-lg",
                                                inputClassName="btn-check",
                                                labelClassName="btn btn-outline-secondary",
                                                labelCheckedClassName="active",
                                            ),
                                        ],
                                        width="auto",
                                    )
                                ],
                                id="container-metricas-maquinas",
                                className="mb-3 justify-content-center",
                                style={"display": "none"},  # Inicialmente escondido
                            ),
                        ],
                        className="pb-3",
                    ),
                    id="colapse-filtros",
                    is_open=False,  # Inicialmente fechado
                ),
                html.Hr(className="m-0"),
                # O botão "Esfera" Centralizado
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "↕",  # Símbolo de setas para cima/baixo (pode trocar por outro emoji ou texto)
                                id="botao-toggle-filtros",
                                color="primary",
                                n_clicks=0,
                                title="Mostrar/Ocultar Filtros",
                                style={
                                    "width": "45px",
                                    "height": "45px",
                                    "borderRadius": "50%",
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "font-size": "22px",
                                    "padding": "0",
                                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.3)",
                                    "transition": "transform 0.2",
                                    "marginTop": "-23px",
                                    "zIndex": "100",
                                    "backgroundColor": "#fff",
                                    "color": "#0d6efd",
                                },
                            ),
                            width=12,
                            className="d-flex justify-content-center mb-4",
                        ),
                    ]
                ),
                # Gráfico Principal
                dbc.Row(
                    [
                        dbc.Col(
                            id="area-conteudo-principal",
                            width=12,
                            className="p-0 border-0",
                            children=[],
                        )
                    ]
                ),
            ],
            fluid=True,
        )


layout = Detalhamento().obter_layout()
