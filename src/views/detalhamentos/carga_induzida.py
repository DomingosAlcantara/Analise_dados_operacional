from dash import html

from src.components.grid import Grid
from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard


class CargaInduzida:
    """Classe responsável pela apresentação do detalhamento da carga induzida."""

    # IDs - Visão Geral
    ID_VALOR_CARGA_INDUZIDA = "detalhamento-val-carga"
    ID_VALOR_MEDIA = "detalhamento-val-media"
    ID_VALOR_RENDIMENTO = "detalhamento-val-rendimento"

    # IDs - Visão Centro
    ID_GRAFICO_CARGA_CENTRO = "detalhamento-graph-carga-centro"
    ID_GRAFICO_RENDIMENTO_CENTRO = "detalhamento-graph-rendimento-centro"
    ID_GRAFICO_CARGA_MAQUINAS = "detalhamento-graph-carga-maquinas"
    ID_GRAFICO_RENDIMENTO_MAQUINAS = "detalhamento-graph-rendimento-maquinas"

    # IDs - Visão Máquina
    ID_GRAFICO_CARGA_TURNO = "detalhamento-graph-carga-turno"
    ID_GRAFICO_RENDIMENTO_TURNO = "detalhamento-graph-rendimento-turno"
    ID_TABELA_PLANOS = "detalhamento-table-planos"
    ID_TEMPO_TURNO1 = "detalhamento-val-tempo-turno1"
    ID_TEMPO_TURNO2 = "detalhamento-val-tempo-turno2"
    ID_TEMPO_TURNO3 = "detalhamento-val-tempo-turno3"
    ID_GRAFICO_CARGA_HORA = "detalhamento-graph-carga-hora"

    def obter_layout(self, nivel="centro"):
        card_carga_detalhes = KpiCard(
            "Carga Induzida", "---", card_id=self.ID_VALOR_CARGA_INDUZIDA
        )
        card_media_carga_detalhes = KpiCard(
            "Média de Carga Induzida", "---", card_id=self.ID_VALOR_MEDIA
        )
        card_rendimento_detalhes = KpiCard(
            "Rendimento Efetivo / h", "---", card_id=self.ID_VALOR_RENDIMENTO
        )

        card_carga_induzida_centro_detalhes = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_CARGA_CENTRO
        )
        card_rendimento_centro_detalhes = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_RENDIMENTO_CENTRO
        )
        card_carga_induzida_maquina_detalhes = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_CARGA_MAQUINAS
        )
        card_rendimento_maquina_detalhes = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_RENDIMENTO_MAQUINAS
        )

        # INSTÂNCIA DOS NOVOS CARDS (VISÃO MÁQUINA)
        card_carga_turno = KpiGraphCard(figure={}, graph_id=self.ID_GRAFICO_CARGA_TURNO)

        card_rendimento_turno = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_RENDIMENTO_TURNO
        )

        card_tabela_planos = html.Div(
            id=self.ID_TABELA_PLANOS,
            style={
                "backgroundColor": "#fff",
                "borderRadius": "8px",
                "padding": "20px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
                "height": "100%",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "color": "#7f8c8d",
                "border": "2px dashed #bdc3c7",
            },
        )

        card_tempo_turno1 = KpiCard(
            "Tempo Turno 1", "---", card_id=self.ID_TEMPO_TURNO1
        )

        card_tempo_turno2 = KpiCard(
            "Tempo Turno 2", "---", card_id=self.ID_TEMPO_TURNO2
        )

        card_tempo_turno3 = KpiCard(
            "Tempo Turno 3", "---", card_id=self.ID_TEMPO_TURNO3
        )

        card_carga_hora = KpiGraphCard(figure={}, graph_id=self.ID_GRAFICO_CARGA_HORA)

        colunas_layout = [
            Grid.coluna(
                children=[
                    card_carga_detalhes.display(),
                    card_media_carga_detalhes.display(),
                    card_rendimento_detalhes.display(),
                ],
                style={
                    "width": "100%",
                    "flex": "1",
                },
            )
        ]

        # Lógica condicional de layout
        if nivel == "centro":
            # Visão do Centro: Mostra os gráficos de carga e rendimento por
            # turno, e os gráficos de carga e rendimento por maquina nos turnos

            colunas_layout.append(
                Grid.coluna(
                    children=[
                        card_carga_induzida_centro_detalhes.display(),
                        card_rendimento_centro_detalhes.display(),
                    ],
                    style={
                        "width": "300px",
                        "flex": "2",
                    },
                )
            )

            colunas_layout.append(
                Grid.coluna(
                    children=[
                        card_carga_induzida_maquina_detalhes.display(),
                        card_rendimento_maquina_detalhes.display(),
                    ],
                    style={
                        "width": "100%",
                        "flex": "5",
                        "minWidth": 0,
                    },
                )
            )

        else:
            # Visão da Maquina: Mostra os gráficos de carga e rendimento por
            # turno, e os gráficos de carga e rendimento por centro nos turnos

            bloco_maquinas = Grid.coluna(
                children=[
                    # Linha 1 - 3 Elementos
                    Grid.linha(
                        children=[
                            Grid.coluna(
                                [
                                    card_carga_turno.display(),
                                ],
                                style={
                                    "flex": "1",
                                    "height": "auto",
                                },
                            ),
                            Grid.coluna(
                                [
                                    card_rendimento_turno.display(),
                                ],
                                style={
                                    "flex": "1",
                                    "height": "auto",
                                },
                            ),
                            Grid.coluna(
                                [
                                    card_tabela_planos,
                                ],
                                style={
                                    "flex": "1.5",
                                    "height": "auto",
                                },
                            ),
                        ],
                        style={
                            "flex": "1",
                        },
                    ),
                    # Linha 2 - 2 Elementos
                    Grid.linha(
                        children=[
                            # Coluna da esquerda (com dois cards empilhados)
                            Grid.coluna(
                                children=[
                                    card_tempo_turno1.display(),
                                    card_tempo_turno2.display(),
                                ],
                                style={
                                    "flex": "1",
                                },
                            ),
                            # Coluna da direita (Gráfico largo)
                            Grid.coluna(
                                children=[
                                    card_carga_hora.display(),
                                ],
                                style={
                                    "flex": "2.5",
                                    "height": "auto",
                                },
                            ),
                        ],
                        style={
                            "flex": "1",
                        },
                    ),
                ],
                style={
                    "width": "100%",
                    "flex": "7",
                    "minWidth": 0,
                    "gap": "10px",
                },
            )

            colunas_layout.append(bloco_maquinas)

        return html.Div(
            children=colunas_layout,
            style={
                "display": "flex",
                "flexDirection": "row",
                "gap": "10px",
                "width": "100%",
                "alignItems": "stretch",
                # --- NOVAS PROPRIEDADES PARA OCULTAR BORDAS ---
                "border": "none",  # Remove qualquer borda sólida
                "boxShadow": "none",  # Remove sombras (que parecem bordas)
                "backgroundColor": "transparent",  # Garante que ele não tenha um fundo diferente
                "padding": "0",  # Remove espaçamentos que causam efeito de borda
            },
            className="kpi-block",
        )


layout = CargaInduzida().obter_layout()
