"""Classe para apresentar o resumo da produtividade e eficiência das
máquinas de triagem de cartas do CTCE.
"""

from datetime import date

import dash
import plotly.express as px
from dash import Input, Output, html

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

            # 3. Construir a view (V) - Usando divs formatadas como blocos / tabelas
            return html.Div(
                [
                    # Bloco principal para o layout (usando flexbox para colunas)
                    html.Div(
                        [
                            # Coluna 1: Carga Induzida
                            html.Div(
                                [
                                    html.P("Carga Induzida", className="kpi-label"),
                                    html.H3(
                                        performance_metrics["carga_induzida"],
                                        className="kpi-value",
                                    ),
                                ],
                                className="kpi-block",
                            ),
                            # Coluna 2: Média de Carga Induzida
                            html.Div(
                                [
                                    html.P("Média de Carga Induzida"),
                                    html.H3(
                                        performance_metrics["media_carga"],
                                        className="kpi-value",
                                    ),
                                ],
                                className="kpi-block",
                            ),
                            # Coluna 3: Rendimento Efetivo / h
                            html.Div(
                                [
                                    html.P(
                                        "Rendimento Efetivo / h", className="kpi-label"
                                    ),
                                    html.H3(
                                        performance_metrics["eficiencia"],
                                        className="kpi-value",
                                    ),
                                ],
                                className="kpi-block",
                            ),
                        ],
                        style={"display": "block", "gap": "5px"},
                    ),
                ],
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
