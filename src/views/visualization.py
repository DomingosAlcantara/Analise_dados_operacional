# # Coluna 2: KPIs por Centro
# html.Div(
#     [
#         card_carga_induzida_centro.display(),
#         card_rendimento_centro.display(),
#     ],
#     style={
#         "display": "flex",
#         "flex-direction": "column",
#         "flex": "1",
#         "height": "70vh",
#     },
#     className="kpi-block",
# ),
# # Coluna 3: Gráficos
# html.Div(
#     [
#         html.Div(
#             [
#                 html.P(
#                     "Carga Induzida por Máquina",
#                     className="kpi-label",
#                 ),
#                 html.Img(
#                     src="/assets/carga_induzida.png",
#                     className="kpi-graph",
#                 ),
#             ],
#             className="kpi-block",
#         ),
#         html.Div(
#             [
#                 html.P(
#                     "Rendimento Efetivo por Máquina",
#                     className="kpi-label",
#                 ),
#                 html.Img(
#                     src="/assets/eficiencia.png",
#                     className="kpi-graph",
#                 ),
#             ],
#             className="kpi-block",
#         ),
#     ],
#     style={
#         "display": "flex",
#         "flex-direction": "column",
#         "height": "70vh",
#         "flex": "1",
#         "minWidth": 0,
#     },
# ),
