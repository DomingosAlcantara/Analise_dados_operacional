"""Classe para apresentar o resumo da produtividade e eficiência das
máquinas de triagem de cartas do CTCE.
"""

import dash
import plotly.express as px
from dash import Input, Output, dcc, html

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
        self.dropdown_id = "resumo-dropdown"
        self.graph_id = "resumo-graph"
        self.register_callbacks()

    def layout(self):
        """Retorna o layout da página de resumo.

        Returns:
            dash.html.Div: Componente Div contendo o layout da página de
            resumo.
        """
        return html.Div(
            [
                html.H1("Carga Induzida - Pitney Bowes", className="page-title"),
                html.Div(className="valores-resumo"),
                dcc.Dropdown(
                    id=self.dropdown_id,
                    options=[
                        {"label": c, "value": c} for c in df["continent"].unique()
                    ],
                    value="Asia",
                    clearable=False,
                    style={"width": "50%"},
                ),
                dcc.Graph(id=self.graph_id),
            ]
        )

    # 3. Método para registrar todos os callbacks da página
    def register_callbacks(self):
        # NOTA: Usamos @callback, que funciona com o dcc.Location no index.py
        # Se você usar @self.app.callback, isso forçará a importação do app de
        # 'app.py'
        @self.app.callback(
            Output(self.graph_id, "figure"),
            Input("global-date-picker", "start_date"),
            Input("global-date-picker", "end_date"),
        )
        def update_figure(selected_continent):
            filtered_df = df[df.continent == selected_continent]

            fig = px.scatter(
                filtered_df,
                x="gdpPercap",
                y="lifeExp",
                size="pop",
                color="country",
                hover_name="country",
                log_x=True,
                size_max=55,
            )
            fig.update_layout(transition_duration=500)
            return fig


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
