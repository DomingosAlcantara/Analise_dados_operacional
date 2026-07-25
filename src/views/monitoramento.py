# """Classe para exibição das opções de detalhamento das métricas"""

# import dash
# import dash_bootstrap_components as dbc
# from dash import Input, Output, dcc, html

# dash.register_page(__name__, path="/detalhamento", name="Detalhamento")


# class Monitoramento:
#     def __init__(self, empresa_model):
#         self._empresa_model = empresa_model

#     def obter_layout(self):
#         """
#         Retorna o layout da página de detalhamento.

#         Returns:
#             html.Div: Layout da página.
#         """
#         return dbc.Container(
#             [
#                 html.H3(
#                     "Detalhamento Operacional",
#                     className="mt-4 mb-4 text-primary text-center",
#                 ),
#                 # Nível 1 - Centro vs Máquinas
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             [
#                                 html.Label(
#                                     "Visão Geral:",
#                                     className="fw-bold d-block mb-1 text-center",
#                                 ),
#                                 dbc.RadioItems(
#                                     id="detalhamento-nivel-1",
#                                     options=[
#                                         {
#                                             "label": "Centro de Tratamento",
#                                             "value": "centro",
#                                         },
#                                         {"label": "Máquinas", "value": "maquinas"},
#                                     ],
#                                     value="centro",
#                                     inline=True,
#                                     className="btn-group",
#                                     inputClassName="btn-check",
#                                     labelClassName="btn btn-outline-primary",
#                                     labelCheckedClassName="active",
#                                 ),
#                             ],
#                             width="auto",
#                         ),
#                     ],
#                     className="mb-3 justify-content-center",
#                 ),
#                 # Nível 2 - Sub-opções dinâmicas
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             id="detalhamento-container-nivel-2",
#                             width="auto",
#                         )
#                     ],
#                     className="mb-3 justify-content-center",
#                 ),
#                 # Nível 3 - Métricas da Máquina
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             id="detalhamento-container-nivel-3",
#                             width="auto",
#                         )
#                     ],
#                     className="mb-4 justify-content-center",
#                 ),
#                 html.Hr(),
#                 # Área de Gráficos e Tabelas
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             [
#                                 dcc.Graph(id="detalhamento-grafico-principal"),
#                             ],
#                             width=12,
#                         ),
#                     ]
#                 ),
#             ],
#             fluid=True,
#         )

#     def register_callbacks(self, app):
#         """Registra os callbacks necessários no aplicativo Dash

#         Args:
#             app (dash.Dash): Instância do aplicativo Dash.
#         """

#         @app.callback(
#             Output("detalhamento-container-nivel-2", "children"),
#             Input("detalhamento-nivel-1", "value"),
#         )
#         def _renderizar_nivel_2(tipo_selecionado):
#             """Renderiza o conteúdo do Nível 2 com base na seleção do Nível 1

#             Args:
#                 tipo_selecionado (str): Valor selecionado no Nível 1.

#             Returns:
#                 html.Div: Conteúdo do Nível 2.
#             """
#             if tipo_selecionado == "centro":
#                 return [
#                     html.Label(
#                         "Métricas do Centro:",
#                         className="fw-bold d-block mb-1 text-center",
#                     ),
#                     dbc.RadioItems(
#                         id="detalhamento-metricas-centro",
#                         options=[
#                             {"label": "Carga Induzida", "value": "carga"},
#                             {"label": "Atolamentos", "value": "atolamentos"},
#                             {"label": "Falhas Técnicas", "value": "falhas_tecnicas"},
#                             {"label": "Rejeitos", "value": "rejeitos"},
#                         ],
#                         value="carga",
#                         inline=True,
#                         className="btn-group",
#                         inputClassName="btn-check",
#                         labelClassName="btn btn-outline-secundary",
#                         labelCheckedClassName="active",
#                     ),
#                 ]
#             else:
#                 # Busca as máquinas diretamente da Model selecionada
#                 opcoes_maquinas = self._empresa_model.listar_maquinas()
#                 return [
#                     html.Label(
#                         "Selecione a Máquina:",
#                         className="fw-bold d-block mb-1 text-center",
#                     ),
#                     dbc.RadioItems(
#                         id="detalhamento-selecao-maquina",
#                         options=opcoes_maquinas,
#                         value=opcoes_maquinas[0] if opcoes_maquinas else None,
#                         inline=True,
#                         className="btn-group",
#                         inputClassName="btn-check",
#                         labelClassName="btn btn-outline-info",
#                         labelCheckedClassName="active",
#                     ),
#                 ]

#         @app.callback(
#             Output("detalhamento-container-nivel-3", "children"),
#             Input("detalhamento-nivel-1", "value"),
#         )
#         def _renderizar_nivel_3(tipo_selecionado):
#             """Renderiza o conteúdo do Nível 3 com base nas seleções dos Níveis 1 e 2

#             Args:
#                 tipo_selecionado (str): Valor selecionado no Nível 1.

#             Returns:
#                 html.Div: Conteúdo do Nível 3.
#             """
#             if tipo_selecionado == "maquinas":
#                 return [
#                     html.Label(
#                         "Métricas da Máquina:",
#                         className="fw-bold d-block mb-1 text-center",
#                     ),
#                     dbc.RadioItems(
#                         id="detalhamento-metricas-maquinas",
#                         options=[
#                             {"label": "Carga Induzida", "value": "carga"},
#                             {"label": "Atolamentos", "value": "atolamentos"},
#                             {"label": "Falhas Técnicas", "value": "falhas_tecnicas"},
#                             {"label": "Rejeitos", "value": "rejeitos"},
#                         ],
#                         value="carga",
#                         inline=True,
#                         className="btn-group",
#                         inputClassName="btn-check",
#                         labelClassName="btn btn-outline-secundary",
#                         labelCheckedClassName="active",
#                     ),
#                 ]
#             return []  # Retorna vazio se não houver seleção válida

#         @app.callback(
#             Output("detalhamento-grafico-principal", "figure"),
#             [
#                 Input("detalhamento-nivel-1", "value"),
#                 Input("detalhamento-container-nivel-2", "children"),
#                 Input("detalhamento-container-nivel-3", "children"),
#             ],
#         )
#         def _atualizar_graficos(nivel1, container_nivel_2, container_nivel_3):
#             """Atualiza os gráficos com base nas seleções dos Níveis 1, 2 e 3

#             Args:
#                 nivel1 (str): Valor selecionado no Nível 1.
#                 container_nivel_2 (list): Conteúdo do Nível 2.
#                 container_nivel_3 (list): Conteúdo do Nível 3.

#             Returns:
#                 plotly.graph_objs._figure.Figure: Gráfico atualizado.
#             """
#             # Lógica para atualizar o gráfico com base nas seleções
#             # Aqui você pode acessar os valores selecionados nos níveis 2 e 3
#             # e gerar o gráfico correspondente usando Plotly ou outra biblioteca.

#             import plotly.express as px

#             return px.bar(
#                 title=f"Gráfico de Detalhamento - Visão: {nivel1.capitalize()}"
#             )


# def get_layout():
#     from src.app import app

#     return Monitoramento(app, register_callbacks=False).obter_layout()


# layout = get_layout
