"""Classe para apresentar o resumo da produtividade e eficiência das
máquinas de triagem de cartas do CTCE.
"""

import dash
from dash import html

from src.components.grid import Grid
from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard

try:
    dash.register_page(__name__, path="/resumos/carga-induzida", name="Carga Induzida")
except Exception:
    # Em ambientes de teste o app pode não estar instanciado ainda. Ignoramos
    # o erro para permitir a importação do módulo sem uma instância do app.
    pass


class CargaInduzida:
    """Classe responsável pela apresentação do resumo da carga induzida."""

    ID_VALOR_CARGA_INDUZIDA = "resumo-val-carga"
    ID_VALOR_MEDIA = "resumo-val-media"
    ID_VALOR_RENDIMENTO = "resumo-val-rendimento"
    ID_GRAFICO_CARGA_CENTRO = "graph-carga-centro"
    ID_GRAFICO_RENDIMENTO_CENTRO = "graph-rendimento-centro"
    ID_GRAFICO_CARGA_MAQUINAS = "graph-carga-maquinas"
    ID_GRAFICO_RENDIMENTO_MAQUINAS = "graph-rendimento-maquinas"

    def obter_layout(self) -> html.Div:
        """Retorna o layout da página de resumo.

        Returns:
            dash.html.Div: Componente Div contendo o layout da página de
            resumo.
        """
        card_carga = KpiCard(
            "Carga Induzida", "---", card_id=self.ID_VALOR_CARGA_INDUZIDA
        )
        card_media_carga = KpiCard(
            "Média de Carga Induzida", "---", card_id=self.ID_VALOR_MEDIA
        )
        card_rendimento = KpiCard(
            "Rendimento Efetivo / h", "---", card_id=self.ID_VALOR_RENDIMENTO
        )

        card_carga_induzida_centro = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_CARGA_CENTRO
        )
        card_rendimento_centro = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_RENDIMENTO_CENTRO
        )
        card_carga_induzida_maquina = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_CARGA_MAQUINAS
        )
        card_rendimento_maquina = KpiGraphCard(
            figure={}, graph_id=self.ID_GRAFICO_RENDIMENTO_MAQUINAS
        )

        return html.Div(
            [
                # Coluna 1: Kpi's
                Grid.coluna(
                    children=[
                        card_carga.display(),
                        card_media_carga.display(),
                        card_rendimento.display(),
                    ],
                    style={
                        "width": "100%",
                        "flex": "1",
                    },
                ),
                # Coluna 2: Gráficos por Centro
                Grid.coluna(
                    children=[
                        card_carga_induzida_centro.display(),
                        card_rendimento_centro.display(),
                    ],
                    style={
                        "width": "300px",
                        "flex": "2",
                    },
                ),
                # Coluna 3: Gráficos por Máquina
                Grid.coluna(
                    children=[
                        card_carga_induzida_maquina.display(),
                        card_rendimento_maquina.display(),
                    ],
                    style={
                        "width": "100%",
                        "flex": "5",
                        "minWidth": 0,
                    },
                ),
            ],
            className="kpi-table",
        )


# Instanciamos a View e deixamos o médoto para o Dash ler
layout = CargaInduzida().obter_layout()
