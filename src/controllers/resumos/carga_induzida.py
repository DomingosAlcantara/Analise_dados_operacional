from datetime import date

from dash import ClientsideFunction, Input, Output, callback, clientside_callback

from src.engine import empresa
from src.models.resumo_model import ResumoModel
from src.utils.colors import get_color_palette

# Importando a classe da view
from src.views.resumos.carga_induzida import CargaInduzida as CargaInduzidaView


class CargaInduzida:
    """Classe responsável por gerenciar a lógica e atualizar a View de Carga
    Induzida.
    """

    def __init__(self):
        # O controller é quem manda no Model
        self._model = ResumoModel(empresa)
        # Referenciamos a classe da View para usar os IDs no callback
        self._view = CargaInduzidaView()

    def registrar_callbacks(self):
        """Registra os callbacks da página de carga induzida"""

        # 1. PROCESSAMENTO BACKEND (Gera o JSON puro)
        @callback(
            Output(self._view.ID_STORE_DADOS, "data"),
            [
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def processar_dados(start_date_str, end_date_str):
            if not start_date_str or not end_date_str:
                return {}

            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)

            metricas = self._model.get_performance_metrics(start_date, end_date)

            df_carga_centro = self._model.carga_induzida_por_centro().reset_index()
            df_rend_centro = self._model.rendimento_efetivo_por_centro().reset_index()
            df_carga_maq = self._model.carga_induzida_por_maquina()
            df_rend_maq = self._model.rendimento_efetivo_por_maquina()

            # Adiciona as cores para o JS usar
            df_carga_centro["cor"] = [
                get_color_palette(c) for c in df_carga_centro["Centro de Tratamento"]
            ]
            df_rend_centro["cor"] = [
                get_color_palette(c) for c in df_rend_centro["Centro de Tratamento"]
            ]
            df_carga_maq["cor"] = [
                get_color_palette(c) for c in df_carga_maq["Centro de Tratamento"]
            ]
            df_rend_maq["cor"] = [
                get_color_palette(c) for c in df_rend_maq["Centro de Tratamento"]
            ]

            # Retorna o dicionário (JSON)
            return {
                "kpis": {
                    "carga": metricas.get("carga_induzida", 0),
                    "media": metricas.get("media_carga", 0),
                    "rendimento": metricas.get("eficiencia", 0),
                },
                "graficos": {
                    "carga_centro": df_carga_centro.to_dict("records"),
                    "rend_centro": df_rend_centro.to_dict("records"),
                    "carga_maquinas": df_carga_maq.to_dict("records"),
                    "rend_maquinas": df_rend_maq.to_dict("records"),
                },
            }

        # 2. RENDERIZAÇÃO FRONTEND (Dispara o JS do arquivo carga_induzida.js)
        clientside_callback(
            ClientsideFunction(
                namespace="carga_induzida_resumo", function_name="renderizar_tela"
            ),
            [
                Output(self._view.ID_VALOR_CARGA_INDUZIDA, "children"),
                Output(self._view.ID_VALOR_MEDIA, "children"),
                Output(self._view.ID_VALOR_RENDIMENTO, "children"),
                Output(self._view.ID_GRAFICO_CARGA_CENTRO, "figure"),
                Output(self._view.ID_GRAFICO_RENDIMENTO_CENTRO, "figure"),
                Output(self._view.ID_GRAFICO_CARGA_MAQUINAS, "figure"),
                Output(self._view.ID_GRAFICO_RENDIMENTO_MAQUINAS, "figure"),
            ],
            Input(self._view.ID_STORE_DADOS, "data"),
            prevent_initial_call=True,
        )
