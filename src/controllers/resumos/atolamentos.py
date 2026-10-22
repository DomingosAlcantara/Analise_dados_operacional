from dash import (
    ClientsideFunction,
    Input,
    Output,
    callback,
    clientside_callback,
)

from src.engine import empresa
from src.utils.colors import get_color_palette
from src.views.resumos.atolamentos import AtolamentosView


class AtolamentosController:
    def __init__(self, empresa_instancia=None):
        self._view = AtolamentosView()
        self._empresa = empresa_instancia or empresa

    def processar_atualizacao_do_dashboard(self, start_date_str, end_date_str):
        if hasattr(self._empresa, "definir_intervalo_de_pesquisa"):
            self._empresa.definir_intervalo_de_pesquisa(start_date_str, end_date_str)

        atolamentos_mgr = self._empresa.atolamentos

        # ---------------------------------------------------------
        # 1. Coleta de Dados Crus (Modelos / Regras de Negócio)
        # ---------------------------------------------------------

        # Tabelas
        df_tabela_centro = atolamentos_mgr.resumo_tempo_por_centro()
        df_tabela_centro["Centro de Tratamento"] = df_tabela_centro[
            "Centro de Tratamento"
        ].str.replace("<br>", " ")
        df_tabela_med = atolamentos_mgr.resumo_tempo_por_maquina()
        df_tabela_med["Nº Máquina"] = (
            df_tabela_med["Nº Máquina"].str.split("<br>").str[-1]
        )

        # Gráficos
        df_grafico_centro_qtd = atolamentos_mgr.por_centro()
        df_grafico_centro_qtd["cor"] = [
            get_color_palette(c) for c in df_grafico_centro_qtd["Centro de Tratamento"]
        ]
        df_grafico_centro_med = (
            atolamentos_mgr.media_objetos_induzidos_por_atolamentos_nos_centros(
                self._empresa.retornar_carga_induzida_total()
            )
        )
        df_grafico_centro_med["cor"] = [
            get_color_palette(c) for c in df_grafico_centro_med["Centro de Tratamento"]
        ]
        df_grafico_maq_qtd = atolamentos_mgr.por_maquina()
        df_grafico_maq_qtd["cor"] = [
            get_color_palette(c) for c in df_grafico_maq_qtd["Centro de Tratamento"]
        ]
        df_grafico_maq_med = (
            atolamentos_mgr.media_objetos_induzidos_por_atolamentos_por_maquina(
                self._empresa.retornar_carga_induzida_total()
            )
        )
        df_grafico_maq_med["cor"] = [
            get_color_palette(c) for c in df_grafico_maq_med["Centro de Tratamento"]
        ]

        return {
            "kpis": {
                "total_atolamentos": atolamentos_mgr.total(),
                "media_atolamentos": atolamentos_mgr.media_diaria(),
                "tempo_total_atolamentos": atolamentos_mgr.tempo_total(),
                "media_obj_atolamentos": atolamentos_mgr.media_objetos_por_atolamento(
                    self._empresa.retornar_carga_induzida_total()
                ),
                "media_diaria_objetos_atolamentos": 0,
            },
            "graficos": {
                "qtd_centro": df_grafico_centro_qtd.to_dict("records"),
                "qtd_maquina": df_grafico_maq_qtd.to_dict("records"),
                "media_centro": df_grafico_centro_med.to_dict("records"),
                "media_maquina": df_grafico_maq_med.to_dict("records"),
            },
            "tabelas": {
                "tempo_centro": {
                    "data": df_tabela_centro.to_dict("records"),
                    "columns": [
                        {"name": col, "id": col} for col in df_tabela_centro.columns
                    ],
                },
                "tempo_maquina": {
                    "data": df_tabela_med.to_dict("records"),
                    "columns": [
                        {"name": col, "id": col} for col in df_tabela_med.columns
                    ],
                },
            },
        }

    def registrar_callbacks(self):
        @callback(
            Output(self._view.ID_STORE_ATOLAMENTOS, "data"),
            [
                Input("tabs-atolamentos", "value"),
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def update_dashboard(aba_ativa, start_date_str, end_date_str):
            # if aba_ativa != "tab-quantidade-atolamentos":
            #     return no_update

            return self.processar_atualizacao_do_dashboard(start_date_str, end_date_str)

        clientside_callback(
            ClientsideFunction(
                namespace="atolamentos_resumo",
                function_name="renderizar_tela",
            ),
            [
                # Outputs dos KPIs (Fixos na esquerda)
                Output(self._view.ID_TOTAL_ATOLAMENTOS, "children"),
                Output(self._view.ID_MEDIA_ATOLAMENTOS, "children"),
                Output(self._view.ID_TEMPO_TOTAL_ATOLAMENTOS, "children"),
                Output(self._view.ID_MEDIA_OBJETOS_POR_ATOLAMENTOS, "children"),
                Output(self._view.ID_MEDIA_DIARIA_OBJETOS_POR_ATOLAMENTOS, "children"),
                # Aba 1: Quantidade
                Output(self._view.ID_QTD_ATOLAMENTOS_CENTRO, "figure"),
                Output(self._view.ID_QTD_ATOLAMENTOS_MAQUINAS, "figure"),
                Output(self._view.ID_TABELA_TEMPO_CENTRO, "data"),
                Output(self._view.ID_TABELA_TEMPO_CENTRO, "columns"),
                # Aba 2: Média
                Output(self._view.ID_MED_OBJ_POR_ATOL, "figure"),
                Output(self._view.ID_MED_OBJ_POR_ATOL_MAQ, "figure"),
                Output(self._view.ID_TABELA_TEMPO_MAQ, "data"),
                Output(self._view.ID_TABELA_TEMPO_MAQ, "columns"),
            ],
            Input(self._view.ID_STORE_ATOLAMENTOS, "data"),
            prevent_initial_call=True,
        )
