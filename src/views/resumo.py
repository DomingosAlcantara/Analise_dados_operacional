"""Classe para apresentar o resumo da produtividade e eficiência das
máquinas de triagem de cartas do CTCE.
"""

from datetime import date

import dash
import plotly.express as px
from dash import Input, Output, html

from src.components.kpi_card import KpiCard

dash.register_page(__name__, path="/", name="Resumo")

# --- Dados de Exemplo ---
df = px.data.gapminder().query("year == 2007")
# ------------------------


class ResumoPage:
    """Classe para apresentar o resumo da produtividade e eficiência das
    máquinas de triagem de cartas do CTCE.
    """

    def __init__(self, app_instance):
        """Inicializa a classe Resumo."""
        self.app = app_instance
        self.kpi_table_id = "resumo-kpi-table"
        self.register_callbacks()

    def layout(self):
        """Retorna o layout da página de resumo.

        Returns:
            dash.html.Div: Componente Div contendo o layout da página de
            resumo.
        """
        return html.Div(
            [
                html.H1("Resumo Geral da Operação", className="page-title"),
                html.Div(id=self.kpi_table_id, style={"marginBottom": "30px"}),
            ]
        )

    # 3. Método para registrar todos os callbacks da página
    def register_callbacks(self):
        # NOTA: Usamos @callback, que funciona com o dcc.Location no index.py
        # Se você usar @self.app.callback, isso forçará a importação do app de
        # 'app.py'
        @self.app.callback(
            Output(self.kpi_table_id, "children"),
            Input("global-date-picker", "start_date"),
            Input("global-date-picker", "end_date"),
        )
        def update_kpi_table(start_date_str, end_date_str):
            # 1. Validação e Conversão (C)
            if not start_date_str or not end_date_str:
                return html.P("Selecione um intervalo de datas válido.")

            # Converter de string para datetime
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)

            # 2. Chamar o modelo (C -> M)
            from src.models.resumo_model import ResumoModel

            resumo_model = ResumoModel(dados=[])  # Dados vazios para exemplo
            performance_metrics = resumo_model.get_performance_metrics(
                start_date, end_date
            )

            # Instanciando os componentes (Objetos)
            card_carga = KpiCard(
                "Carga Induzida",
                performance_metrics["carga_induzida"],
                card_id="kpi-carga-induzida",
            )

            card_media_carga = KpiCard(
                "Média de Carga Induzida",
                performance_metrics["media_carga"],
                card_id="kpi-media-carga",
            )

            card_rendimento = KpiCard(
                "Rendimento Efetivo / h",
                performance_metrics["eficiencia"],
                card_id="kpi-rendimento",
            )

            card_carga_induzida_centro = KpiCard(
                "Carga Induzida por Centro",
                "777",  # performance_metrics["carga_induzida_centro"]
                card_id="kpi-carga-induzida-centro",
            )

            card_rendimento_centro = KpiCard(
                "Rendimento Efetivo por Centro",
                "555",  # performance_metrics["rendimento_centro"]
                card_id="kpi-rendimento-centro",
            )

            # 3. Construir a view (V) - Usando divs formatadas como blocos / tabelas
            # Bloco principal para o layout (usando flexbox para colunas)
            return html.Div(
                [
                    # Coluna 1: Carga Induzida
                    html.Div(
                        [
                            card_carga.display(),
                            card_media_carga.display(),
                            card_rendimento.display(),
                        ],
                        style={
                            "display": "flex",
                            "flex-direction": "column",
                            # "flex-wrap": "wrap",
                            "height": "75vh",
                            "width": "100%",
                            "flex": "1",
                            "gap": "0px",
                        },
                    ),
                    # Coluna 2: KPIs por Centro
                    html.Div(
                        [
                            card_carga_induzida_centro.display(),
                            card_rendimento_centro.display(),
                        ],
                        style={
                            "display": "flex",
                            "flex-direction": "column",
                            "height": "75vh",
                            "width": "100%",
                            "flex": "1.5",
                            "gap": "0px",
                        },
                    ),
                    # Coluna 3: Gráficos
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(
                                        "Carga Induzida por Máquina",
                                        className="kpi-label",
                                    ),
                                    html.Img(
                                        src="/assets/carga_induzida.png",
                                        className="kpi-graph",
                                    ),
                                ],
                                className="kpi-block",
                            ),
                            html.Div(
                                [
                                    html.P(
                                        "Rendimento Efetivo por Máquina",
                                        className="kpi-label",
                                    ),
                                    html.Img(
                                        src="/assets/eficiencia.png",
                                        className="kpi-graph",
                                    ),
                                ],
                                className="kpi-block",
                            ),
                        ],
                        style={
                            "display": "flex",
                            "flex-direction": "column",
                            "height": "75vh",
                            "width": "100%",
                            "flex": "5",
                            "minWidth": 0,
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    # "flex-wrap": "wrap",
                    "height": "75vh",
                    "width": "100%",
                    "flex": "1",
                    "gap": "0px",
                },
                className="kpi-table",
            )


# 4. INSTÂNCIA E ATRIBUIÇÃO FINAL:
# Agora, você só pode instanciar depois que o app for importado no index.py
# Modifique o final do arquivo para:
def get_layout():
    """Função para retornar o layout da página Resumo.

    Returns:
        dash.html.Div: Componente Div contendo o layout da página de resumo.
    """
    # Primeiro, importamos a instância do app:
    from src.app import app  # noqa F401

    resumo_page_instance = ResumoPage(app)
    return resumo_page_instance.layout()


# A variável global 'layout' deve ser uma FUNÇÃO que o Dash pode chamar
# para evitar o carregamento imediato da instância do app.
layout = get_layout
