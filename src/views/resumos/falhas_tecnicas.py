import dash
import dash_bootstrap_components as dbc
from dash import html

from src.components.grid import Grid
from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard

try:
    dash.register_page(
        __name__, path="/resumos/falhas-tecnicas", name="Falhas Técnicas"
    )
except Exception:
    # Em ambientes de teste o app pode não estar instanciado ainda. Ignoramos
    # o erro para permitir a importação do módulo sem uma instância do app.
    pass


class FalhasTecnicasView:
    """
    View para exibir o resumo de falhas técnicas,
    """

    # IDs - KPIs
    ID_TOTAL_FALHAS = "resumo-total-falhas"
    ID_MEDIA_OBJETOS_POR_FALHAS = "resumo-media-objetos-por-falhas"
    ID_TEMPO_TOTAL_OCORRENCIAS = "resumo-tempo-total-ocorrencias"
    ID_DURACAO_MEDIA_FALHAS = "resumo-duracao-media-falhas"

    # IDs - Aba1: Quantidades
    ID_GRAFICO_CENTRO_QTD = "grafico-falhas-por-centro-qtd"
    ID_GRAFICO_MAQUINAS_QTD = "grafico-falhas-por-maquinas-qtd"
    ID_TABELA_MAQUINAS_QTD = "tabela-falhas-por-maquinas-qtd"

    # IDs - Aba2: Médias
    ID_GRAFICO_CENTRO_MED = "grafico-falhas-por-centro-med"
    ID_GRAFICO_MAQUINAS_MED = "grafico-falhas-por-maquinas-med"
    ID_TABELA_MAQUINAS_MED = "tabela-falhas-por-maquinas-med"

    def layout(self) -> html.Div:
        """
        Retorna o layout da página de falhas técnicas.

        Returns:
            html.Div: Componente Div contendo o layout da página.
        """

        card_total_falhas = KpiCard(
            "Total de Falhas",
            "---",
            card_id=self.ID_TOTAL_FALHAS,
        )

        card_media_objetos_falhas = KpiCard(
            "Média de Objetos por Falhas",
            "---",
            card_id=self.ID_MEDIA_OBJETOS_POR_FALHAS,
        )

        card_tempo_total_ocorrencias = KpiCard(
            "Tempo Total de Ocorrências",
            "---",
            card_id=self.ID_TEMPO_TOTAL_OCORRENCIAS,
        )

        card_duracao_media_falhas = KpiCard(
            "Duração Média das Falhas",
            "---",
            card_id=self.ID_DURACAO_MEDIA_FALHAS,
        )

        # Componentes da aba 1: Quantidades
        grafico_centro_qtd = KpiGraphCard(
            figure={},
            graph_id=self.ID_GRAFICO_CENTRO_QTD,
        )

        grafico_maquina_qtd = KpiGraphCard(
            figure={},
            graph_id=self.ID_GRAFICO_MAQUINAS_QTD,
        )

        # Placeholder da futura tabela
        tabela_qtd = html.Div(
            "Tabela de Quantidade por máquina",
            id=self.ID_TABELA_MAQUINAS_QTD,
            style={
                "backgroundColor": "#fff",
                "borderRadius": "8px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "height": "100%",
                "border": "2px dashed #bdc3c7",
                "color": "#7f8c8d",
            },
        )

        # Componentes da aba 2: Médias
        grafico_centro_med = KpiGraphCard(
            figure={},
            graph_id=self.ID_GRAFICO_CENTRO_MED,
        )

        grafico_maquina_med = KpiGraphCard(
            figure={},
            graph_id=self.ID_GRAFICO_MAQUINAS_MED,
        )

        # Placeholder da futura tabela
        tabela_med = html.Div(
            "Tabela de Médias por máquina",
            id=self.ID_TABELA_MAQUINAS_MED,
            style={
                "backgroundColor": "#fff",
                "borderRadius": "8px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "height": "100%",
                "border": "2px dashed #bdc3c7",
                "color": "#7f8c8d",
            },
        )

        conteudo_aba_quantidade = html.Div(
            [
                Grid.linha(
                    [
                        Grid.coluna(
                            [grafico_centro_qtd.display()],
                            style={
                                "flex": "3.5",
                                "height": "375px",
                            },
                        ),
                        Grid.coluna(
                            [tabela_qtd],
                            style={
                                "flex": "1.5",
                                "height": "375px",
                            },
                        ),
                    ],
                ),
                Grid.linha(
                    [
                        Grid.coluna(
                            [
                                grafico_maquina_qtd.display(),
                            ],
                            style={
                                "flex": "1",
                                "height": "375px",
                            },
                        )
                    ],
                ),
            ]
        )

        conteudo_aba_medias = html.Div(
            [
                Grid.linha(
                    [
                        Grid.coluna(
                            [grafico_centro_med.display()],
                            style={
                                "flex": "3.5",
                                "height": "375px",
                            },
                        ),
                        Grid.coluna(
                            [tabela_med],
                            style={
                                "flex": "1.5",
                                "height": "375px",
                            },
                        ),
                    ],
                ),
                Grid.linha(
                    [
                        Grid.coluna(
                            [
                                grafico_maquina_med.display(),
                            ],
                            style={
                                "flex": "1",
                                "height": "375px",
                            },
                        )
                    ],
                ),
            ]
        )

        # Definindo o estilo das abas INATIVAS
        estilos_aba_inativa = {
            "minWidth": "min-content",
            "textAlign": "center",
            "padding": "12px 25px",
            "whiteSpace": "nowrap",
            "display": "inline-block",
            "boxSizing": "border-box",
            "backgroundColor": "#f0f2f5",
            "color": "#546e7a",
            "fontWeight": "bold",
            "border": "1px solid #dee2e6",
            "borderBottom": "none",
            "borderRadius": "8px 8px 0 0",
            "marginRight": "5px",
        }

        estilos_aba_ativa = {
            "minWidth": "min-content",
            "textAlign": "center",
            "backgroundColor": "#1890ff",
            "color": "#ffffff",
            "border": "1px solid #1890ff",
            "borderBottom": "none",
        }

        # Criar o container de Tabs
        painel_tabs = dbc.Tabs(
            [
                dbc.Tab(
                    conteudo_aba_quantidade,
                    label="Quantidades",
                    tab_id="tab_qtd",
                    label_style=estilos_aba_inativa,
                    active_label_style=estilos_aba_ativa,
                ),
                dbc.Tab(
                    conteudo_aba_medias,
                    label="Médias",
                    tab_id="tab_med",
                    label_style=estilos_aba_inativa,
                    active_label_style=estilos_aba_ativa,
                ),
            ],
            active_tab="tab_qtd",
            style={
                "borderBottom": "2px solid #1890ff",
            },
        )

        coluna_esquerda = Grid.coluna(
            [
                card_total_falhas.display(),
                card_media_objetos_falhas.display(),
                card_tempo_total_ocorrencias.display(),
                card_duracao_media_falhas.display(),
            ],
            style={
                "flex": "1",
                "display": "flex",
                "flex-direction": "column",
            },
        )

        coluna_direita = Grid.coluna(
            [painel_tabs],
            style={
                "flex": "7",
                "display": "flex",
                "flex-direction": "column",
            },
        )

        return html.Div(
            [
                Grid.linha(
                    [
                        coluna_esquerda,
                        coluna_direita,
                    ]
                )
            ],
        )


#     def register_callbacks(self):
#         """
#         Registra os callbacks necessários para a página.

#         Args:
#             app (dash.Dash): Instância do aplicativo Dash.
#         """

#         @callback(
#             [
#                 Output(self._TOTAL_FALHAS, "children"),
#                 Output(self._MEDIA_OBJETOS_POR_FALHAS, "children"),
#                 Output(self._TEMPO_TOTAL_OCORRENCIAS, "children"),
#                 Output(self._DURACAO_MEDIA_FALHAS, "children"),
#                 Output("grafico-falhas-por-centro", "figure"),
#                 Output("grafico-falhas-por-maquina", "figure"),
#             ],
#             [
#                 Input("global-date-picker", "start_date"),
#                 Input("global-date-picker", "end_date"),
#             ],
#         )
#         def update_falhas_tecnicas(start_date_str, end_date_str):
#             # Lógica para atualizar o conteúdo com base no valor de entrada
#             return self.falhas_kpis_e_graficos(start_date_str, end_date_str)

#     def falhas_kpis_e_graficos(self, start_date_str, end_date_str):
#         # Lógica para calcular os KPIs e gerar os gráficos com base no
#         # intervalo de datas
#         # Aqui você pode acessar os dados, aplicar filtros e retornar os
#         # valores atualizados

#         start_date = date.fromisoformat(start_date_str)
#         end_date = date.fromisoformat(end_date_str)

#         metricas = self._resumo_model.retornar_metricas_falhas_tecnicas(
#             start_date, end_date
#         )
#         return (
#             str(
#                 metricas.get("total_de_falhas", 0)
#             ),  # Exemplo de valor atualizado para o total de falhas
#             str(
#                 metricas.get("media_objetos_por_falha", 0)
#             ),  # Exemplo de valor atualizado para a média de objetos por falhas
#             "----",  # Exemplo de valor atualizado para o tempo total de ocorrências
#             "----",  # Exemplo de valor atualizado para a duração média das falhas
#             {},  # Exemplo de figura atualizada para o gráfico de falhas por centro
#             {},  # Exemplo de figura atualizada para o gráfico de falhas por máquina
#         )


# def get_layout() -> html.Div:
#     """
#     Retorna o layout completo da página, incluindo callbacks.

#     Returns:
#         html.Div: Componente Div contendo o layout da página.
#     """
#     return FalhasTecnicasView(register_callbacks=False).layout()


layout = FalhasTecnicasView().layout()
