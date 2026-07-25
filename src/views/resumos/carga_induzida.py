"""Classe para apresentar o resumo da produtividade e eficiência das
máquinas de triagem de cartas do CTCE.
"""

from datetime import date, timedelta

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, html
from plotly import express as px

from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard
from src.engine import empresa
from src.models.resumo_model import ResumoModel
from src.views.colors import get_color_palette

try:
    dash.register_page(__name__, path="/resumos/carga-induzida", name="Carga Induzida")
except Exception:
    # Em ambientes de teste o app pode não estar instanciado ainda. Ignoramos
    # o erro para permitir a importação do módulo sem uma instância do app.
    pass


class CargaInduzida:
    """Classe para apresentar o resumo da produtividade e eficiência das
    máquinas de triagem de cartas do CTCE.
    """

    def __init__(self, model_instance=None, register_callbacks=True):
        """Inicializa a classe Resumo."""
        # self.app = app_instance
        self.ID_VALOR_CARGA_INDUZIDA = "resumo-val-carga"
        self.ID_VALOR_MEDIA = "resumo-val-media"
        self.ID_VALOR_RENDIMENTO = "resumo-val-rendimento"

        # Inicializando o modelo de resumo
        self._resumo_model = ResumoModel(empresa)

        # Calcula métricas iniciais usando o intervalo padrão (últimos 30 dias)
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=30)
            self._initial_metrics = self._resumo_model.get_performance_metrics(
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

    def gerar_graficos(
        self,
        df,
        coluna_x,
        coluna_y,
        titulo,
        eh_por_centro=True,
        aplicar_ordenacao=False,
        sort_columns=None,
        usar_rotulo_maquina=False,
    ):
        """Gera um gráfico de barras padronizado.

        Args:
            dados: DataFrame ou Series com os dados
            coluna_x: Nome da coluna para eixo X
            coluna_y: Nome da coluna para eixo Y
            titulo: Título do gráfico
            eh_por_centro: Se True, aplica cores por Centro de Tratamento
            aplicar_sort: Se True, ordena os dados
            sort_columns: Lista de colunas para ordenação [col1, col2]
            usar_rotulo_maquina: Se True, aplica rótulo formatado para máquinas

        Returns:
            go.Figure: Figura Plotly pronta para renderizar
        """
        if df is None or df.empty:
            return px.bar(title=titulo)

        # Converter Series para DataFrame se necessário
        if not isinstance(df, pd.DataFrame):
            df = df.reset_index()
        else:
            df = df.copy()

        if aplicar_ordenacao and sort_columns:
            df = df.sort_values(by=sort_columns, ascending=[True, False])

        # Aplicar rótulo formatado para máquinas
        if usar_rotulo_maquina:
            df = self._resumo_model._adicionar_rotulo_maquina(df)
            coluna_x_display = "Rótulo Máquina"
        else:
            coluna_x_display = coluna_x

        # Determinar cores
        if eh_por_centro and "Centro de Tratamento" in df.columns:
            colors_map = get_color_palette(df["Centro de Tratamento"])  # type: ignore
            cores_atribuidas = [colors_map[name] for name in df["Centro de Tratamento"]]  # type: ignore
        else:
            cores_atribuidas = None

        texts = [
            self._resumo_model.formatacao_compacta_de_valores(val)
            for val in df[coluna_y]
        ]

        # Criar figura
        figura = go.Figure(
            data=go.Bar(
                x=df[coluna_x_display],
                y=df[coluna_y],
                text=texts,
                marker_color=cores_atribuidas,
                textposition="outside",
                textfont={"size": 18},
            )
        )

        # Aplicar formatação padrao
        figura.update_traces(texttemplate="%{text}")
        figura.update_layout(
            title={
                "text": titulo,
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                "font": {
                    "size": 25,
                    "color": "black",
                },
            },
            xaxis=dict(
                type="category" if coluna_x == "Nº Máquina" else None,
                # tickmode="array",
                tickvals=df[coluna_x_display],
                ticktext=(
                    [str(m).replace(" ", "<br>") for m in df[coluna_x_display]]
                    if coluna_x_display != "Rótulo Máquina"
                    else None
                ),
            ),
        )

        figura.update_yaxes(range=[0, df[coluna_y].max() * 1.15])

        return figura

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
            className="kpi-table",
        )

    # 3. Método para registrar todos os callbacks da página
    def register_callbacks(self):
        # Registramos o callback que delega a lógica para `compute_kpis`.
        @callback(
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

        try:
            performance_metrics = self._resumo_model.get_performance_metrics(
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
        fig_carga = self.gerar_graficos(
            self._resumo_model.carga_induzida_por_centro(),
            coluna_x="Centro de Tratamento",
            coluna_y="Quantidade Induzida",
            titulo="Carga Induzida por Centro",
        )

        fig_rend = self.gerar_graficos(
            self._resumo_model.rendimento_efetivo_por_centro(),
            coluna_x="Centro de Tratamento",
            coluna_y="Rendimento Efetivo Médio",
            titulo="Rendimento Efetivo por Centro",
        )

        # # Gerar gráfico de carga por máquina com ordenação dupla
        fig_carga_maquina = self.gerar_graficos(
            self._resumo_model.carga_induzida_por_maquina().sort_values(
                by=["Centro de Tratamento", "Quantidade Induzida"],
                ascending=[True, False],
            ),
            coluna_x="Nº Máquina",
            coluna_y="Quantidade Induzida",
            titulo="Carga Induzida por Máquina",
            usar_rotulo_maquina=False,  # True para usar rótulo formatado, False para usar Nº Máquina
        )

        fig_rend_maquina = self.gerar_graficos(
            self._resumo_model.rendimento_efetivo_por_maquina().sort_values(
                by=["Centro de Tratamento", "Rendimento Efetivo Médio"],
                ascending=[True, False],
            ),
            coluna_x="Nº Máquina",
            coluna_y="Rendimento Efetivo Médio",
            titulo="Rendimento Efetivo por Máquina",
            usar_rotulo_maquina=False,  # True para usar rótulo formatado, False para usar Nº Máquina
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
    return CargaInduzida(register_callbacks=False).layout()


# A variável global 'layout' deve ser uma FUNÇÃO que o Dash pode chamar
# para evitar o carregamento imediato da instância do app.
layout = get_layout
