from dash import html

from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard
from src.components.kpi_table_card import KPITableCard


class DashboardContainer:
    """
    Classe responsável exclusivamente pelo layout estrutural das telas de monitoramento.

    Aplica a divisão proporcional de espaço:
    - 1/8 da largura para a área lateral de KPIs.
    - 7/8 da largura para a área principal de Abas (Gráficos/Tabelas).
    """

    def __init__(
        self,
        kpis: list[html.Div | KpiCard] | None = None,
        abas: list[KpiGraphCard | KPITableCard] | None = None,
    ):
        """
        Inicializa o container estrutural.

        Args:
            kpis (list, optional): Lista de componentes de KPI a serem
            renderizados na coluna da esquerda.
            tabs_content (dcc.Tabs | html.Div, optional): Componente de Abas
            ou contêiner principal para a direita.
        """
        self.kpis = kpis if kpis is not None else []
        self.tabs_content = abas if abas is not None else html.Div()

    def layout(self) -> html.Div:
        """ "
        Monta o esqueleto visual do container com as classes isoladas.

        Returns:
            html.Div: Div contendo a estrutura de 2 colunas proporcional.
        """

        return html.Div(
            className="ctce-dashboard-container",
            children=[
                # Coluna de KPIs (1/8 do espaço)
                html.Div(
                    className="ctce-kpi-column",
                    children=self.kpis,
                ),
                # Coluna Principal de Abas/Gráficos (7/8 do espaço)
                html.Div(
                    className="ctce-tabs-column",
                    children=self.tabs_content,
                ),
            ],
        )
