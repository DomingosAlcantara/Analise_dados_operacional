import dash
from dash import dcc, html

from src.components.dashboard_container import DashboardContainer
from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard
from src.components.kpi_table_card import KPITableCard

try:
    dash.register_page(
        __name__, path="/resumos/falhas-tecnicas", name="Falhas Técnicas"
    )
except Exception:
    pass


class FalhasTecnicasView:
    ID_TOTAL_FALHAS = "resumo-total-falhas"
    ID_MEDIA_OBJETOS_POR_FALHA = "resumo-media-objetos-por-falhas"
    ID_TEMPO_TOTAL_OCORRENCIAS = "resumo-tempo-total-ocorrencias"
    ID_DURACAO_MEDIA_FALHAS = "resumo-duracao-media-falhas"
    ID_GRAFICO_CENTRO_QTD = "grafico-qtd-falhas-centro"
    ID_GRAFICO_MAQUINA_QTD = "grafico-qtd-falhas-maquina"
    ID_TABELA_CENTRO_QTD = "tabela-qtd-falhas-centro"
    ID_GRAFICO_CENTRO_MED = "grafico-med-falhas-centro"
    ID_GRAFICO_MAQUINA_MED = "grafico-med-falhas-maquina"
    ID_TABELA_MAQUINA_MED = "tabela-med-falhas-centro"

    def layout(self) -> html.Div:
        # Instanciação dos 4 KPIs

        card_total_falhas = KpiCard(
            "Total de Falhas", "---", card_id=self.ID_TOTAL_FALHAS
        )
        card_media_objetos_falhas = KpiCard(
            "Média de Objetos por Falhas",
            "---",
            card_id=self.ID_MEDIA_OBJETOS_POR_FALHA,
        )
        card_tempo_total_ocorrencias = KpiCard(
            "Tempo Total de Ocorrências", "---", card_id=self.ID_TEMPO_TOTAL_OCORRENCIAS
        )
        card_duracao_media_falhas = KpiCard(
            "Duração Média das Falhas", "---", card_id=self.ID_DURACAO_MEDIA_FALHAS
        )

        kpis_topo = [
            card_total_falhas.display(),
            card_media_objetos_falhas.display(),
            card_tempo_total_ocorrencias.display(),
            card_duracao_media_falhas.display(),
        ]

        # -----------------------------------------------------------
        # ABA 1: QUANTIDADES
        # -----------------------------------------------------------
        aba_quantidade = dcc.Tab(
            label="Quantidade",
            value="tab-quantidade",
            className="custom-tab",
            selected_className="custom-tab-selected",
            children=[
                html.Div(
                    [
                        # Linha Superior: Gráfico horizontal (60%) e Tabela (40%)
                        html.Div(
                            [
                                KpiGraphCard(
                                    graph_id="grafico-qtd-falhas-centro",
                                    extra_class="tab-item-grafico",
                                ).display(),
                                KPITableCard(
                                    table_id=self.ID_TABELA_CENTRO_QTD,
                                    dados=None,
                                    extra_class="tab-item-tabela",
                                    colunas_esquerda=["Centro de Tratamento"],
                                ).display(),
                            ],
                            className="tab-row-superior",
                        ),
                        KpiGraphCard(
                            graph_id="grafico-qtd-falhas-maquina",
                            extra_class="tab-row-inferior",
                        ).display(),
                    ],
                    className="tabs-content-container",
                )
            ],
        )

        # -----------------------------------------------------------
        # ABA 2: MÉDIAS
        # -----------------------------------------------------------
        aba_medias = dcc.Tab(
            label="Médias",
            value="tab-medias",
            className="custom-tab",
            selected_className="custom-tab-selected",
            children=[
                html.Div(
                    [
                        # Linha Superior: Gráfico horizontal (60%) e Tabela (40%)
                        html.Div(
                            [
                                KpiGraphCard(
                                    graph_id=self.ID_GRAFICO_CENTRO_MED,
                                    extra_class="tab-item-grafico",
                                ).display(),
                                KPITableCard(
                                    table_id=self.ID_TABELA_MAQUINA_MED,
                                    dados=None,
                                    extra_class="tab-item-tabela",
                                ).display(),
                            ],
                            className="tab-row-superior",
                        ),
                        KpiGraphCard(
                            graph_id=self.ID_GRAFICO_MAQUINA_MED,
                            extra_class="tab-row-inferior",
                        ).display(),
                    ],
                    className="tabs-content-container",
                )
            ],
        )

        # Estrutura principal com o dcc.Tabs
        area_graficos_tabelas = html.Div(
            dcc.Tabs(
                id="tabs-falhas",
                value="tab-quantidade",
                children=[
                    aba_quantidade,
                    aba_medias,
                ],
            ),
            className="coluna-direita-tabs",
        )

        container = DashboardContainer(kpis=kpis_topo, abas=area_graficos_tabelas)

        return html.Div(
            container.layout(),
            className="tela-no-scroll",
        )


layout = FalhasTecnicasView().layout()
