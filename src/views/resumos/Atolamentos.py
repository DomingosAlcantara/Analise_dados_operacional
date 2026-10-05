import dash
from dash import html

from src.components.dashboard_container import DashboardContainer
from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard
from src.components.kpi_table_card import KPITableCard

try:
    dash.register_page(__name__, path="/resumos/atolamentos", name="Atolamentos")
except Exception:
    # Em ambientes de teste o app pode não estar instanciado ainda. Ignoramos
    # o erro para permitir a importação do módulo sem uma instância do app.
    pass


class AtolamentosView:
    def __init__(self):
        self.ID_STORE_ATOLAMENTOS = "store-atolamentos"
        # IDs Visão Geral
        self.ID_TOTAL_ATOLAMENTOS = "resumo-total-atolamentos"
        self.ID_MEDIA_ATOLAMENTOS = "resumo-media-diaria-atolamentos"
        self.ID_TEMPO_TOTAL_ATOLAMENTOS = "resumo-tempo-total-atolamentos"
        self.ID_MEDIA_OBJETOS_POR_ATOLAMENTOS = "resumo-media-objetos-por-atolamentos"
        self.ID_MEDIA_DIARIA_OBJETOS_POR_ATOLAMENTOS = (
            "resumo-media-diaria-objetos-por-atolamentos"
        )

        # ID Visão Quantidade
        self.ID_QTD_ATOLAMENTOS_CENTRO = "resumo-qtd-atolamentos-centro"
        self.ID_QTD_ATOLAMENTOS_MAQUINAS = "resumo-qtd-atolamentos-maquinas"
        self.ID_TABELA_TEMPO_CENTRO = "resumo-tabela-tempo-centro"

        # ID Visão Média
        self.ID_MED_OBJ_POR_ATOL = "resumo-media-objetos-por-atolamento"
        self.ID_MED_OBJ_POR_ATOL_MAQ = "resumo-media-objetos-por-atolamento-maquinas"
        self.ID_TABELA_TEMPO_MAQ = "resumo-tabela-tempo-maquinas"

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

        card_media_objetos_por_atolamentos = KpiCard(
            "Média de Objetos por Atolamentos",
            value="---",
            card_id=self.ID_MEDIA_OBJETOS_POR_ATOLAMENTOS,
        )

        card_media_diaria_objetos_por_atolamentos = KpiCard(
            "Média Diária de Objetos por Atolamentos",
            value="---",
            card_id=self.ID_MEDIA_DIARIA_OBJETOS_POR_ATOLAMENTOS,
        )

        graph_atolamentos_centro = KpiGraphCard(
            figure={},
            graph_id=self.ID_QTD_ATOLAMENTOS_CENTRO,
            extra_class="tab-item-grafico",
        )

        card_tabela_tempo_centro = KPITableCard(
            table_id=self.ID_TABELA_TEMPO_CENTRO,
            dados=None,
            extra_class="tab-item-tabela",
        )

        graph_atolamentos_maquina = KpiGraphCard(
            figure={},
            graph_id=self.ID_QTD_ATOLAMENTOS_MAQUINAS,
            extra_class="tab-row-inferior",
        )

        graph_media_objetos_por_atolamentos = KpiGraphCard(
            figure={},
            graph_id=self.ID_MED_OBJ_POR_ATOL,
            extra_class="tab-item-grafico",
        )

        graph_media_objetos_por_atolamentos_maquina = KpiGraphCard(
            figure={},
            graph_id=self.ID_MED_OBJ_POR_ATOL_MAQ,
            extra_class="tab-row-inferior",
        )

        card_tabela_tempo_maquina = KPITableCard(
            table_id=self.ID_TABELA_TEMPO_MAQ,
            dados=None,
            extra_class="tab-item-tabela",
        )

        kpis = [
            card_total_atolamentos.display(),
            card_media_atolamentos.display(),
            card_tempo_total_atolamentos.display(),
            card_media_objetos_por_atolamentos.display(),
            card_media_diaria_objetos_por_atolamentos.display(),
        ]

        # -----------------------------------------------------------
        # ABA 1: QUANTIDADES
        # -----------------------------------------------------------
        aba_quantidade = dash.dcc.Tab(
            label="Quantidade",
            value="tab-quantidade-atolamentos",
            className="custom-tab",
            selected_className="custom-tab-selected",
            children=[
                html.Div(
                    [
                        # Linha Superior: Gráfico horizontal (60%) e Tabela (40%)
                        html.Div(
                            [
                                graph_atolamentos_centro.display(),
                                card_tabela_tempo_centro.display(),
                            ],
                            className="tab-row-superior",
                        ),
                        # Linha Inferior: Gráfico horizontal (100%)
                        graph_atolamentos_maquina.display(),
                    ],
                    className="tabs-content-container",
                )
            ],
        )

        # -----------------------------------------------------------
        # ABA 2: MÉDIAS
        # -----------------------------------------------------------
        aba_media = dash.dcc.Tab(
            label="Médias",
            value="tab-medias-atolamentos",
            className="custom-tab",
            selected_className="custom-tab-selected",
            children=[
                html.Div(
                    [
                        # Linha Superior: Gráfico horizontal (60%) e Tabela (40%)
                        html.Div(
                            [
                                graph_media_objetos_por_atolamentos.display(),
                                card_tabela_tempo_maquina.display(),
                            ],
                            className="tab-row-superior",
                        ),
                        # Linha Inferior: Gráfico horizontal (100%)
                        graph_media_objetos_por_atolamentos_maquina.display(),
                    ],
                    className="tabs-content-container",
                )
            ],
        )

        # Estrutura principal com o dcc.Tabs
        area_graficos_tabelas = html.Div(
            dash.dcc.Tabs(
                id="tabs-atolamentos",
                value="tab-quantidade-atolamentos",
                children=[
                    aba_quantidade,
                    aba_media,
                ],
            ),
            className="coluna-direita-tabs",
        )

        container = DashboardContainer(
            kpis=kpis,
            abas=area_graficos_tabelas,
        )

        return html.Div(
            [
                dash.dcc.Store(id=self.ID_STORE_ATOLAMENTOS),
                container.layout(),
            ],
            className="tela-no-scroll",
        )


layout = AtolamentosView().obter_layout()
