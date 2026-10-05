from dash import ClientsideFunction, Input, Output, callback, clientside_callback

from src.engine import empresa
from src.utils.colors import get_color_palette
from src.views.resumos.falhas_tecnicas import FalhasTecnicasView


class FalhasTecnicasController:

    def __init__(self, empresa_instancia=None):
        self._view = FalhasTecnicasView()
        self._empresa = empresa_instancia or empresa

    def processar_atualizacao_do_dashboard(self, start_date_str, end_date_str):
        self._empresa = self._empresa.definir_intervalo_de_pesquisa(
            start_date_str, end_date_str
        )

        # ---------------------------------------------------------
        # 1. Coleta de Dados Crus (Modelos / Regras de Negócio)
        # ---------------------------------------------------------

        # Tabelas
        df_tabela_centro = self._empresa.retornar_resumo_tempo_por_centro()
        df_tabela_centro["Centro de Tratamento"] = df_tabela_centro[
            "Centro de Tratamento"
        ].str.replace("<br>", " ")
        df_tabela_med = self._empresa.retornar_resumo_tempo_por_maquina()
        df_tabela_med["Máquina"] = df_tabela_med["Máquina"].str.split("<br>").str[-1]

        # Gráficos
        df_grafico_centro_qtd = self._empresa.retornar_total_falhas_por_centro()
        df_grafico_centro_qtd["cor"] = [
            get_color_palette(c) for c in df_grafico_centro_qtd["Centro de Tratamento"]
        ]
        df_grafico_centro_med = self._empresa.retornar_duracao_media_falhas_por_centro()
        df_grafico_centro_med["cor"] = [
            get_color_palette(c) for c in df_grafico_centro_med["Centro de Tratamento"]
        ]
        df_grafico_maq_qtd = self._empresa.retornar_total_falhas_por_maquina()
        df_grafico_maq_qtd = df_grafico_maq_qtd.sort_values(
            by=["Centro de Tratamento", "Total de Falhas"], ascending=[True, False]
        )
        df_grafico_maq_qtd["cor"] = [
            get_color_palette(c) for c in df_grafico_maq_qtd["Centro de Tratamento"]
        ]
        df_grafico_maq_med = self._empresa.retornar_duracao_media_falhas_por_maquina()
        df_grafico_maq_med = df_grafico_maq_med.sort_values(
            by=["Centro de Tratamento", "Duração Média"], ascending=[True, False]
        )
        df_grafico_maq_med["cor"] = [
            get_color_palette(c) for c in df_grafico_maq_med["Centro de Tratamento"]
        ]

        # ---------------------------------------------------------
        # 2. Montagem do Payload JSON (Data Transfer Object)
        # ---------------------------------------------------------
        payload = {
            "kpis": {
                "total": self._empresa.retornar_total_de_falhas(),
                "media": self._empresa.retornar_media_de_objetos_por_falha(),
                "tempo_total": self._empresa.retornar_tempo_total_de_ocorrencias(),
                "duracao_media": self._empresa.retornar_duracao_media_das_falhas(),
            },
            "graficos": {
                "centro_qtd": df_grafico_centro_qtd.to_dict("records"),
                "maquina_qtd": df_grafico_maq_qtd.to_dict("records"),
                "centro_med": df_grafico_centro_med.to_dict("records"),
                "maquina_med": df_grafico_maq_med.to_dict("records"),
            },
            "tabelas": {
                "centro_qtd": {
                    "data": df_tabela_centro.to_dict("records"),
                    "columns": [
                        {"name": col, "id": col} for col in df_tabela_centro.columns
                    ],
                },
                "maquina_med": {
                    "data": df_tabela_med.to_dict("records"),
                    "columns": [
                        {"name": col, "id": col} for col in df_tabela_med.columns
                    ],
                },
            },
        }

        return payload

    def registrar_callbacks(self):
        @callback(
            Output(self._view.ID_STORE_FALHAS, "data"),
            [
                # Inputs das datas
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def update_dashboard(start_date_str, end_date_str):
            return self.processar_atualizacao_do_dashboard(start_date_str, end_date_str)

        # Callback JavaScript: Renderiza a tela (Frontend)
        clientside_callback(
            ClientsideFunction(
                namespace="falhas_tecnicas_resumo",
                function_name="renderizar_tela",
            ),
            [
                # Outputs dos KPIs (Fixos na esquerda)
                Output(self._view.ID_TOTAL_FALHAS, "children"),
                Output(self._view.ID_MEDIA_OBJETOS_POR_FALHA, "children"),
                Output(self._view.ID_TEMPO_TOTAL_OCORRENCIAS, "children"),
                Output(self._view.ID_DURACAO_MEDIA_FALHAS, "children"),
                # # Outputs da aba 1: Quantidades
                Output(self._view.ID_GRAFICO_CENTRO_QTD, "figure"),
                Output(self._view.ID_GRAFICO_MAQUINA_QTD, "figure"),
                # Output da Aba 1: Tabela
                Output(self._view.ID_TABELA_CENTRO_QTD, "data"),
                Output(self._view.ID_TABELA_CENTRO_QTD, "columns"),
                # # Outputs da aba 2: Médias
                Output(self._view.ID_GRAFICO_CENTRO_MED, "figure"),
                Output(self._view.ID_GRAFICO_MAQUINA_MED, "figure"),
                # Output da Aba 2: Tabela
                Output(self._view.ID_TABELA_MAQUINA_MED, "data"),
                Output(self._view.ID_TABELA_MAQUINA_MED, "columns"),
            ],
            Input(self._view.ID_STORE_FALHAS, "data"),
        )
