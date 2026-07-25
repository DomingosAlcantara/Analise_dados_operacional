"""Classe que executará todo o controle (callbacks) sobre a classe 'views.detalhamento'"""

import dash_bootstrap_components as dbc
from dash import Input, Output, callback, html

from src.engine import empresa


class Detalhamento:

    def __init__(self):
        """O controller conecta a View aos dados (Model)"""
        self._empresa_model = empresa

    def registrar_callbacks(self):
        """Registra os callbacks da página de detalhamento"""

        @callback(
            Output("detalhamento-container-nivel-2", "children"),
            Input("detalhamento-nivel-1", "value"),
        )
        def _renderizar_nivel_2(tipo_selecionado):
            """Renderiza o conteudo do nível 2 com base na seleção do nível 1

            Args:
                tipo_selecionado (str): Valor selecionado no nível 1.

            Returns:
                html.Div: Conteudo do nível 2.
            """
            if tipo_selecionado == "centro":
                return [
                    html.Label(
                        "Métricas do Centro:",
                        className="fw-bold d-block mb-1 text-center",
                    ),
                    dbc.RadioItems(
                        id="detalhamento-metricas-centro",
                        options=[
                            {"label": "Carga Induzida", "value": "carga"},
                            {"label": "Atolamentos", "value": "atolamentos"},
                            {"label": "Falhas Técnicas", "value": "falhas_tecnicas"},
                            {"label": "Rejeitos", "value": "rejeitos"},
                        ],
                        value="carga",
                        inline=True,
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-secondary",
                        labelCheckedClassName="active",
                    ),
                ]
            else:
                # Busca as máquinas diretamente da Model selecionada
                opcoes_maquinas = [
                    {"label": f"PBVS {i}", "value": f"PBVS{i}"}
                    for i in range(
                        1, 4
                    )  # Ou dinâmico via self.empresa_model] #self._empresa_model.listar_maquinas()
                ]
                return [
                    html.Label(
                        "Selecione a Máquina:",
                        className="fw-bold d-block mb-1 text-center",
                    ),
                    dbc.RadioItems(
                        id="detalhamento-selecao-maquina",
                        options=opcoes_maquinas,
                        value=opcoes_maquinas[0] if opcoes_maquinas else None,
                        inline=True,
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-info",
                        labelCheckedClassName="active",
                    ),
                ]

        @callback(
            Output("detalhamento-container-nivel-3", "children"),
            Input("detalhamento-nivel-1", "value"),
        )
        def _renderizar_nivel_3(tipo_selecionado):
            """Renderiza o conteúdo do Nível 3 com base nas seleções dos Níveis 1 e 2

            Args:
                tipo_selecionado (str): Valor selecionado no Nível 1.

            Returns:
                html.Div: Conteúdo do Nível 3.
            """
            if tipo_selecionado == "maquinas":
                return [
                    html.Label(
                        "Métricas da Máquina:",
                        className="fw-bold d-block mb-1 text-center",
                    ),
                    dbc.RadioItems(
                        id="detalhamento-metricas-maquinas",
                        options=[
                            {"label": "Carga Induzida", "value": "carga"},
                            {"label": "Atolamentos", "value": "atolamentos"},
                            {"label": "Falhas Técnicas", "value": "falhas_tecnicas"},
                            {"label": "Rejeitos", "value": "rejeitos"},
                        ],
                        value="carga",
                        inline=True,
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-secondary",
                        labelCheckedClassName="active",
                    ),
                ]
            return []  # Retorna vazio se não houver seleção válida

        @callback(
            Output("detalhamento-grafico-principal", "figure"),
            [
                Input("detalhamento-nivel-1", "value"),
                Input("detalhamento-container-nivel-2", "children"),
                Input("detalhamento-container-nivel-3", "children"),
            ],
        )
        def _atualizar_graficos(nivel1, container_nivel_2, container_nivel_3):
            """Atualiza os gráficos com base nas seleções dos Níveis 1, 2 e 3

            Args:
                nivel1 (str): Valor selecionado no Nível 1.
                container_nivel_2 (list): Conteúdo do Nível 2.
                container_nivel_3 (list): Conteúdo do Nível 3.

            Returns:
                plotly.graph_objs._figure.Figure: Gráfico atualizado.
            """
            # Lógica para atualizar o gráfico com base nas seleções
            # Aqui você pode acessar os valores selecionados nos níveis 2 e 3
            # e gerar o gráfico correspondente usando Plotly ou outra biblioteca.

            import plotly.express as px

            return px.bar(
                title=f"Gráfico de Detalhamento - Visão: {nivel1.capitalize()}"
            )
