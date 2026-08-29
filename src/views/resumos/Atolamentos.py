import dash
from dash import html

from src.components.grid import Grid
from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard

try:
    dash.register_page(__name__, path="/resumos/atolamentos", name="Atolamentos")
except Exception:
    # Em ambientes de teste o app pode não estar instanciado ainda. Ignoramos
    # o erro para permitir a importação do módulo sem uma instância do app.
    pass


class AtolamentosView:
    def __init__(self):
        # IDs Visão Geral
        self.ID_TOTAL_ATOLAMENTOS = "resumo-total-atolamentos"
        self.ID_MEDIA_ATOLAMENTOS = "resumo-media-diaria-atolamentos"
        self.ID_TEMPO_TOTAL_ATOLAMENTOS = "resumo-tempo-total-atolamentos"

        # ID Visão Centro
        self.ID_QTD_ATOLAMENTOS_CENTRO = "resumo-qtd-atolamentos-centro"
        self.ID_QTD_ATOLAMENTOS_MAQUINAS = "resumo-qtd-atolamentos-maquinas"
        self.ID_TABELA_TEMPO_CENTRO = "resumo-tabela-tempo-centro"

    def obter_layout(self):
        card_total_atolamentos = KpiCard(
            "Total de Atolamentos",
            value="---",
            card_id=self.ID_TOTAL_ATOLAMENTOS,
        )

        card_media_atolamentos = KpiCard(
            "Média de Atolamentos / Dia",
            value="---",
            card_id=self.ID_MEDIA_ATOLAMENTOS,
        )

        card_tempo_total_atolamentos = KpiCard(
            "Tempo Total de Atolamentos",
            value="---",
            card_id=self.ID_TEMPO_TOTAL_ATOLAMENTOS,
        )

        card_atolamentos_centro = KpiGraphCard(
            figure={},
            graph_id=self.ID_QTD_ATOLAMENTOS_CENTRO,
        )

        card_tabela_tempo_centro = html.Div(
            id=self.ID_TABELA_TEMPO_CENTRO,
            style={"height": "100%", "width": "100%"},
        )

        card_atolamentos_maquina = KpiGraphCard(
            figure={},
            graph_id=self.ID_QTD_ATOLAMENTOS_MAQUINAS,
        )

        layout = [
            # Coluna dos kpis
            Grid.coluna(
                children=[
                    card_total_atolamentos.display(),
                    card_media_atolamentos.display(),
                    card_tempo_total_atolamentos.display(),
                ],
                style={"width": "100%", "flex": "1"},
            ),
            # Linha com gráfico e tabela
            Grid.linha(
                children=[
                    card_atolamentos_centro.display(),
                    card_tabela_tempo_centro,
                ],
                style={"width": "100%", "flex": "2"},
            ),
            Grid.linha(
                children=[
                    card_atolamentos_maquina.display(),
                ],
                style={"width": "100%", "flex": "2"},
            ),
        ]

        return Grid.coluna(
            children=layout,
            style={
                "display": "flex",
                "flex-direction": "row",
            },
        )


layout = AtolamentosView().obter_layout()
