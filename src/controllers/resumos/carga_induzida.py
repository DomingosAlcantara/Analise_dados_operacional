from datetime import date

from dash import Input, Output, callback
from plotly import express as px

from src.engine import empresa
from src.models.resumo_model import ResumoModel
from src.utils.colors import get_color_palette
from src.utils.graficos import Graficos

# Importando a classe da view
from src.views.resumos.carga_induzida import CargaInduzida as CargaInduzidaView


class CargaInduzida:
    """Classe responsável por gerenciar a lógica e atualizar a View de Carga
    Induzida.
    """

    def __init__(self):
        # O controller é quem manda no Model
        self._resumo_model = ResumoModel(empresa)
        # Referenciamos a classe da View para usar os IDs no callback
        self._view = CargaInduzidaView()

    def registrar_callbacks(self):
        """Registra os callbacks da página de carga induzida"""

        @callback(
            [
                Output(self._view.ID_VALOR_CARGA_INDUZIDA, "children"),
                Output(self._view.ID_VALOR_MEDIA, "children"),
                Output(self._view.ID_VALOR_RENDIMENTO, "children"),
                Output(self._view.ID_GRAFICO_CARGA_CENTRO, "figure"),
                Output(self._view.ID_GRAFICO_RENDIMENTO_CENTRO, "figure"),
                Output(self._view.ID_GRAFICO_CARGA_MAQUINAS, "figure"),
                Output(self._view.ID_GRAFICO_RENDIMENTO_MAQUINAS, "figure"),
            ],
            [
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def update_kpi_table(start_date_str, end_date_str):
            """Atualiza os KPIs e gráficos da página de carga induzida com base nas datas selecionadas.

            Args:
                start_date_str (str): Data de início selecionada no date picker.
                end_date_str (str): Data de término selecionada no date picker.

            Returns:
                tuple: Valores atualizados dos KPIs e figuras dos gráficos.
            """
            if not start_date_str or not end_date_str:
                msg = "-"
                empty_fig = px.bar(title="Aguardando datas...")
                return msg, msg, msg, empty_fig, empty_fig, empty_fig, empty_fig

            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)

            try:
                metricas = self._resumo_model.get_performance_metrics(
                    start_date, end_date
                )
            except Exception as e:
                print(f"Erro ao calcular métricas: {e}")
                msg = "-"
                empty_fig = px.bar(title="Erro ao carregar dados")
                return msg, msg, msg, empty_fig, empty_fig, empty_fig, empty_fig

            # Preparação dos dados no Controller
            df_carga_centro = (
                self._resumo_model.carga_induzida_por_centro().sort_values(
                    by="Centro de Tratamento", ascending=True
                )
            )
            texts_carga_centro = [
                self._resumo_model.formatacao_compacta_de_valores(val)
                for val in df_carga_centro["Quantidade Induzida"]
            ]

            df_rend_centro = (
                self._resumo_model.rendimento_efetivo_por_centro().sort_values(
                    by="Centro de Tratamento", ascending=True
                )
            )
            texts_rend_centro = [
                self._resumo_model.formatacao_compacta_de_valores(val)
                for val in df_rend_centro["Rendimento Efetivo Médio"]
            ]

            df_carga_maquinas = (
                self._resumo_model.carga_induzida_por_maquina().sort_values(
                    by="Centro de Tratamento", ascending=True
                )
            )
            # df_carga_maquinas =
            texts_carga_maquinas = [
                self._resumo_model.formatacao_compacta_de_valores(val)
                for val in df_carga_maquinas["Quantidade Induzida"]
            ]

            df_rend_maquinas = (
                self._resumo_model.rendimento_efetivo_por_maquina().sort_values(
                    by="Centro de Tratamento", ascending=True
                )
            )
            texts_rend_maquinas = [
                self._resumo_model.formatacao_compacta_de_valores(val)
                for val in df_rend_maquinas["Rendimento Efetivo Médio"]
            ]

            # Geramos o mapa das cores e extraímos a lista exata para o DataFrame Atual
            # mapa_cores = get_color_palette(df_carga_centro["Centro de Tratamento"])
            cores_carga_centro = [
                get_color_palette(centro)
                for centro in sorted(df_carga_centro["Centro de Tratamento"])
            ]

            cores_carga_maquinas = [
                get_color_palette(centro)
                for centro in sorted(df_carga_maquinas["Centro de Tratamento"])
            ]

            # 2. Chamada da classe utilitaria (desacoplada)
            fig_carga = Graficos.gerar_grafico_barras(
                df=df_carga_centro,
                coluna_x="Centro de Tratamento",
                coluna_y="Quantidade Induzida",
                titulo="Carga Induzida por Centro",
                texts=texts_carga_centro,
                cores=cores_carga_centro,
            )

            fig_rend = Graficos.gerar_grafico_barras(
                df=df_rend_centro,
                coluna_x="Centro de Tratamento",
                coluna_y="Rendimento Efetivo Médio",
                titulo="Rendimento Efetivo por Centro",
                texts=texts_rend_centro,
                cores=cores_carga_centro,
            )

            fig_carga_maquinas = Graficos.gerar_grafico_barras(
                df=df_carga_maquinas,
                coluna_x="Nº Máquina",
                coluna_y="Quantidade Induzida",
                titulo="Carga Induzida por Máquina",
                texts=texts_carga_maquinas,
                cores=cores_carga_maquinas,
            )

            fig_rend_maquinas = Graficos.gerar_grafico_barras(
                df=df_rend_maquinas,
                coluna_x="Nº Máquina",
                coluna_y="Rendimento Efetivo Médio",
                titulo="Rendimento Efetivo por Máquina",
                texts=texts_rend_maquinas,
                cores=cores_carga_maquinas,
            )

            return (
                metricas.get("carga_induzida", 0),
                metricas.get("media_carga", 0),
                metricas.get("eficiencia", 0),
                fig_carga,
                fig_rend,
                fig_carga_maquinas,
                fig_rend_maquinas,
            )
