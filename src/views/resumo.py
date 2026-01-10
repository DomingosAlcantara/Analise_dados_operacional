"""Classe para apresentar o resumo da produtividade e eficiência das
máquinas de triagem de cartas do CTCE.
"""

from datetime import date, timedelta

import dash
import plotly.express as px
from dash import Input, Output, html

from src.components.kpi_card import KpiCard
from src.models.carga_induzida_model import CargaInduzidaModel
from src.models.resumo_model import ResumoModel
from src.path_files import PathFiles

try:
    dash.register_page(__name__, path="/", name="Resumo")
except Exception:
    # Em ambientes de teste o app pode não estar instanciado ainda. Ignoramos
    # o erro para permitir a importação do módulo sem uma instância do app.
    pass

# --- Dados de Exemplo ---
df = px.data.gapminder().query("year == 2007")
# ------------------------


class ResumoPage:
    """Classe para apresentar o resumo da produtividade e eficiência das
    máquinas de triagem de cartas do CTCE.
    """

    def __init__(self, app_instance, model_instance=None, register_callbacks=True):
        """Inicializa a classe Resumo."""
        self.app = app_instance
        self.ID_VALOR_CARGA_INDUZIDA = "resumo-val-carga"
        self.ID_VALOR_MEDIA = "resumo-val-media"
        self.ID_VALOR_RENDIMENTO = "resumo-val-rendimento"

        # Inicializando o modelo de carga induzida
        self._carga_induzida = CargaInduzidaModel(path=PathFiles.ARQUIVOS_CARGA_TRATADA)

        # Calcula métricas iniciais usando o intervalo padrão (últimos 30 dias)
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=30)
            resumo_model = ResumoModel(self._carga_induzida)
            self._initial_metrics = resumo_model.get_performance_metrics(
                start_date, end_date
            )
        except Exception as e:
            print(f"Erro calculando métricas iniciais: {e}")
            self._initial_metrics = {
                "carga_induzida": "---",
                "media_carga": "---",
                "eficiencia": "---",
            }

        if register_callbacks:
            self.register_callbacks()

    def layout(self):
        """Retorna o layout da página de resumo.

        Returns:
            dash.html.Div: Componente Div contendo o layout da página de
            resumo.
        """

        # Instanciando os componentes (Objetos)
        card_carga = KpiCard(
            "Carga Induzida",
            self._initial_metrics.get("carga_induzida", "---"),
            card_id=self.ID_VALOR_CARGA_INDUZIDA,
        )

        card_media_carga = KpiCard(
            "Média de Carga Induzida",
            self._initial_metrics.get("media_carga", "---"),
            card_id=self.ID_VALOR_MEDIA,
        )

        card_rendimento = KpiCard(
            "Rendimento Efetivo / h",
            self._initial_metrics.get("eficiencia", "---"),
            card_id=self.ID_VALOR_RENDIMENTO,
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
                        "height": "84vh",
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
                        "height": "84vh",
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
                        "height": "84vh",
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
                "height": "84vh",
                "width": "100%",
                "flex": "1",
                "gap": "0px",
            },
            className="kpi-table",
        )

    # 3. Método para registrar todos os callbacks da página
    def register_callbacks(self):
        # Registramos o callback que delega a lógica para `compute_kpis`.
        @self.app.callback(
            [
                Output(self.ID_VALOR_CARGA_INDUZIDA, "children"),
                Output(self.ID_VALOR_MEDIA, "children"),
                Output(self.ID_VALOR_RENDIMENTO, "children"),
            ],
            [
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def update_kpi_table(start_date_str, end_date_str):
            return self.compute_kpis(start_date_str, end_date_str)

    def compute_kpis(self, start_date_str, end_date_str):
        """Lógica extraída para facilitar testes unitários."""
        # 1. Validação e Conversão (C)
        if not start_date_str or not end_date_str:
            msg = "Selecione um intervalo de datas válido."
            return msg, msg, msg

        # Converter de string para datetime
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        resumo_model = ResumoModel(self._carga_induzida)

        try:
            performance_metrics = resumo_model.get_performance_metrics(
                start_date, end_date
            )
        except Exception:
            return "—", "—", "—"

        return (
            performance_metrics.get("carga_induzida", "—"),
            performance_metrics.get("media_carga", "—"),
            performance_metrics.get("eficiencia", "—"),
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

    # Não re-registrar callbacks novamente (já registramos no startup)
    resumo_page_instance = ResumoPage(app, register_callbacks=False)
    return resumo_page_instance.layout()


# A variável global 'layout' deve ser uma FUNÇÃO que o Dash pode chamar
# para evitar o carregamento imediato da instância do app.
layout = get_layout
