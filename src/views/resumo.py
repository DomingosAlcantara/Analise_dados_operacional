"""Classe para apresentar o resumo da produtividade e eficiência das
máquinas de triagem de cartas do CTCE.
"""

from datetime import date, timedelta

import dash
import plotly.graph_objects as go
from dash import Input, Output, html
from plotly import express as px

from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard
from src.models.carga_induzida_model import CargaInduzidaModel
from src.models.resumo_model import ResumoModel
from src.path_files import PathFiles
from src.views.colors import get_color_palette

try:
    dash.register_page(__name__, path="/", name="Resumo")
except Exception:
    # Em ambientes de teste o app pode não estar instanciado ainda. Ignoramos
    # o erro para permitir a importação do módulo sem uma instância do app.
    pass


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

        card_carga_induzida_centro = KpiGraphCard(
            figure={},
            graph_id="graph-carga-centro",
        )

        card_rendimento_centro = KpiGraphCard(
            figure={},
            graph_id="graph-rendimento-centro",
        )

        card_carga_induzida_maquina = KpiGraphCard(
            figure={},
            graph_id="graph-carga-maquina",
        )

        card_rendimento_maquina = KpiGraphCard(
            figure={},
            graph_id="graph-rendimento-maquina",
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
                # Coluna 2: KPIs por Centro + Gráficos
                html.Div(
                    [
                        card_carga_induzida_centro.display(),
                        card_rendimento_centro.display(),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "height": "84vh",
                        "width": "300px",
                        "flex": "2",
                        "gap": "0px",
                    },
                ),
                # Coluna 3: Gráficos (restaurada)
                html.Div(
                    [
                        card_carga_induzida_maquina.display(),
                        card_rendimento_maquina.display(),
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
                Output("graph-carga-centro", "figure"),
                Output("graph-rendimento-centro", "figure"),
                Output("graph-carga-maquina", "figure"),
                Output("graph-rendimento-maquina", "figure"),
            ],
            [
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def update_kpi_table(start_date_str, end_date_str):
            return self.compute_kpis(start_date_str, end_date_str, include_figures=True)

    def compute_kpis(self, start_date_str, end_date_str, include_figures: bool = False):
        """Lógica extraída para facilitar testes unitários."""
        # 1. Validação e Conversão (C)
        if not start_date_str or not end_date_str:
            msg = "Selecione um intervalo de datas válido."
            return msg, msg, msg

        # Converter de string para datetime
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
        cores_atribuidas = []

        resumo_model = ResumoModel(self._carga_induzida)

        try:
            performance_metrics = resumo_model.get_performance_metrics(
                start_date, end_date
            )
        except Exception:
            if include_figures:
                empty_fig = px.bar(title="Carga Induzida por Centro")
                empty_fig2 = px.bar(title="Rendimento Efetivo por Centro")
                return "—", "—", "—", empty_fig, empty_fig2
            return "—", "—", "—"

        # Se não for necessário gerar figuras (calls de teste), retornamos
        # apenas os 3 KPIs
        if not include_figures:
            return (
                performance_metrics.get("carga_induzida", "—"),
                performance_metrics.get("media_carga", "—"),
                performance_metrics.get("eficiencia", "—"),
            )

        # Gerar gráficos a partir dos dados filtrados no modelo
        # A chamada a get_performance_metrics já filtra os dados no model
        # interno
        serie_carga = resumo_model.carga_induzida_por_centro()

        if serie_carga is None or serie_carga.empty:
            fig_carga = px.bar(title="Carga Induzida por Centro")
        else:
            df_carga = serie_carga.reset_index()
            if df_carga.shape[1] == 2:
                df_carga.columns = ["Centro de Tratamento", "Quantidade Induzida"]
                colors_map = get_color_palette(df_carga["Centro de Tratamento"])  # type: ignore
                cores_atribuidas = [colors_map[name] for name in df_carga["Centro de Tratamento"]]  # type: ignore

            fig_carga = go.Figure(
                data=go.Bar(
                    x=df_carga["Centro de Tratamento"],
                    y=df_carga["Quantidade Induzida"],
                    text=df_carga["Quantidade Induzida"],
                    marker_color=cores_atribuidas,
                    textposition="outside",
                    textfont={
                        "size": 18,
                    },
                )
            )
            fig_carga.update_traces(texttemplate="%{text:.2s}")
            fig_carga.update_layout(
                title={
                    "text": "Carga Induzida por Centro",
                    "y": 0.9,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                    "font": {
                        "size": 20,
                        "color": "black",
                        # "family": "Arial",
                    },
                },
                xaxis=dict(
                    tickmode="array",
                    tickvals=df_carga["Centro de Tratamento"],
                    ticktext=[
                        m.replace(" ", "<br>") for m in df_carga["Centro de Tratamento"]
                    ],
                ),
            )
            fig_carga.update_yaxes(
                range=[0, df_carga["Quantidade Induzida"].max() * 1.15]
            )

        serie_rend = resumo_model.rendimento_efetivo_por_centro()
        if serie_rend is None or serie_rend.empty:
            fig_rend = px.bar(title="Rendimento Efetivo por Centro")
        else:
            df_rend = serie_rend.reset_index()
            if df_rend.shape[1] == 2:
                df_rend.columns = ["Centro de Tratamento", "Rendimento Efetivo/h"]
            fig_rend = go.Figure(
                data=go.Bar(
                    x=df_rend["Centro de Tratamento"],
                    y=df_rend["Rendimento Efetivo/h"],
                    # title="Rendimento Efetivo por Centro",
                    text=df_rend["Rendimento Efetivo/h"],
                    marker_color=cores_atribuidas,
                    textposition="outside",
                    textfont={"size": 18},
                )
            )
            fig_rend.update_traces(texttemplate="%{text:.2s}")
            fig_rend.update_layout(
                title={
                    "text": "Rendimento Efetivo por Centro",
                    "y": 0.9,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                    "font": {
                        "size": 20,
                        "color": "black",
                        # "family": "Arial",
                    },
                },
                xaxis=dict(
                    tickmode="array",
                    tickvals=df_rend["Centro de Tratamento"],
                    ticktext=[
                        m.replace(" ", "<br>") for m in df_rend["Centro de Tratamento"]
                    ],
                ),
            )
            fig_rend.update_yaxes(
                range=[0, df_rend["Rendimento Efetivo/h"].max() * 1.15]
            )

        df_carga_maquina = resumo_model.carga_induzida_por_maquina()
        if df_carga_maquina is None or df_carga_maquina.empty:
            fig_carga_maquina = px.bar(title="Carga Induzida por Máquina")
        else:
            colors_map = get_color_palette(df_carga_maquina["Centro de Tratamento"])  # type: ignore
            cores_atribuidas = [colors_map[name] for name in df_carga_maquina["Centro de Tratamento"]]  # type: ignore
            fig_carga_maquina = go.Figure(
                data=go.Bar(
                    x=df_carga_maquina["Nº Máquina"],
                    y=df_carga_maquina["Quantidade Induzida"],
                    text=df_carga_maquina["Quantidade Induzida"],
                    marker_color=cores_atribuidas,
                    textposition="outside",
                    textfont={"size": 18},
                )
            )

            fig_carga_maquina.update_traces(texttemplate="%{text:.2s}")
            fig_carga_maquina.update_layout(
                title={
                    "text": "Carga Induzida por Máquina",
                    "y": 0.9,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                    "font": {
                        "size": 20,
                        "color": "black",
                        # "family": "Arial",
                    },
                },
                xaxis=dict(
                    type="category",
                    tickvals=df_carga_maquina["Nº Máquina"],
                    # ticktext=[
                    #     m.replace(" ", "<br>") for m in df_carga_maquina["Nº Máquina"]
                    # ],
                ),
            )
            fig_carga_maquina.update_yaxes(
                range=[0, df_carga_maquina["Quantidade Induzida"].max() * 1.15]
            )

        df_rend_maquina = resumo_model.rendimento_efetivo_por_maquina()
        if df_rend_maquina is None or df_rend_maquina.empty:
            fig_rend_maquina = px.bar(title="Rendimento Efetivo por Máquina")
        else:
            colors_map = get_color_palette(df_rend_maquina["Centro de Tratamento"])  # type: ignore
            cores_atribuidas = [colors_map[name] for name in df_rend_maquina["Centro de Tratamento"]]  # type: ignore

            fig_rend_maquina = go.Figure(
                data=go.Bar(
                    x=df_rend_maquina["Nº Máquina"],
                    y=df_rend_maquina["Rendimento Efetivo/h"],
                    text=df_rend_maquina["Rendimento Efetivo/h"],
                    marker_color=cores_atribuidas,
                    textposition="outside",
                    textfont={"size": 18},
                )
            )

            fig_rend_maquina.update_traces(texttemplate="%{text:.2s}")
            fig_rend_maquina.update_layout(
                title={
                    "text": "Rendimento Efetivo por Máquina",
                    "y": 0.9,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                    "font": {
                        "size": 20,
                        "color": "black",
                        # "family": "Arial",
                    },
                },
                xaxis=dict(
                    type="category",
                    tickvals=df_rend_maquina["Nº Máquina"],
                    # ticktext=[
                    #     m.replace(" ", "<br>") for m in df_carga_maquina["Nº Máquina"]
                    # ],
                ),
            )
            fig_rend_maquina.update_yaxes(
                range=[0, df_rend_maquina["Rendimento Efetivo/h"].max() * 1.15]
            )

        return (
            performance_metrics.get("carga_induzida", "—"),
            performance_metrics.get("media_carga", "—"),
            performance_metrics.get("eficiencia", "—"),
            fig_carga,
            fig_rend,
            fig_carga_maquina,
            fig_rend_maquina,
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
