import plotly.express as px
from dash import Input, Output, callback

from src.engine import empresa
from src.models.resumo_model import ResumoModel
from src.utils.colors import MAPA_CORES_CENTROS
from src.utils.formatadores import formatar_tempo_hhmmss
from src.views.resumos.falhas_tecnicas import FalhasTecnicasView


class FalhasTecnicasController:

    def __init__(self, empresa_instancia=None):
        self._view = FalhasTecnicasView()
        self._empresa = empresa_instancia or empresa

    def processar_atualizacao_do_dashboard(self, start_date_str, end_date_str):
        self._empresa = self._empresa.definir_intervalo_de_pesquisa(
            start_date_str, end_date_str
        )

        kpi_total = ResumoModel.formatacao_compacta_de_valores(
            self._empresa.retornar_total_de_falhas()
        )

        kpi_media = ResumoModel.formatacao_compacta_de_valores(
            self._empresa.retornar_media_de_objetos_por_falha()
        )

        kpi_tempo_total = formatar_tempo_hhmmss(
            self._empresa.retornar_tempo_total_de_ocorrencias()
        )

        kpi_duracao_media = formatar_tempo_hhmmss(
            self._empresa.retornar_duracao_media_das_falhas()
        )

        # --- ABA 1: QUANTIDADES ---
        df_centro_qtd = self._empresa.retornar_total_falhas_por_centro()
        df_maquina_qtd = self._empresa.retornar_total_falhas_por_maquina()

        # Gráfico: Total por Centro
        fig_centro_qtd = px.bar(
            df_centro_qtd,
            x="Total de Falhas",
            y="Centro de Tratamento",
            orientation="h",
            text="Total de Falhas",
            color="Centro de Tratamento",
            color_discrete_map=MAPA_CORES_CENTROS,
            title="Total de Falhas por Centro",
            template="plotly_white",
        )
        fig_centro_qtd.update_layout(
            showlegend=False, yaxis={"categoryorder": "total ascending"}
        )

        # Gráfico: Total por Maquina
        fig_maquina_qtd = px.bar(
            df_maquina_qtd,
            x="Nº Máquina",
            y="Total de Falhas",
            text="Total de Falhas",
            color="Centro de Tratamento",
            color_discrete_map=MAPA_CORES_CENTROS,
            title="Total de Falhas por Máquina",
            template="plotly_white",
        )
        fig_maquina_qtd.update_layout(
            showlegend=False,
        )

        # ---------------------------------------------------------
        # Tabela: Resumo de Tempos por Centro (NOVO)
        # ---------------------------------------------------------

        df_tabela_centro = self._empresa.retornar_resumo_tempo_por_centro()

        df_tabela_centro["Centro de Tratamento"] = df_tabela_centro[
            "Centro de Tratamento"
        ].str.replace("<br>", " ")

        # Aplicamos o formatador para que os segundos virem 'HH:MM:SS' na tela
        df_tabela_centro["Tempo Total"] = df_tabela_centro["Tempo Total"].apply(
            formatar_tempo_hhmmss
        )
        df_tabela_centro["Tempo Médio"] = df_tabela_centro["Tempo Médio"].apply(
            formatar_tempo_hhmmss
        )

        dados_tabela_aba1 = df_tabela_centro.to_dict("records")
        colunas_tabela_aba1 = [{"name": i, "id": i} for i in df_tabela_centro.columns]

        # ---------------------------------------------------------
        # ABA 2: MÉDIAS / DURAÇÕES
        # ---------------------------------------------------------
        df_centro_med = self._empresa.retornar_duracao_media_falhas_por_centro()
        df_maquina_med = self._empresa.retornar_duracao_media_falhas_por_maquina()

        # Cria coluna auxiliar formatada para exibir nos rótulos de texto
        df_centro_med["Texto_Formatado"] = df_centro_med["Duração Média"].apply(
            formatar_tempo_hhmmss
        )
        df_maquina_med["Texto_Formatado"] = df_maquina_med["Duração Média"].apply(
            formatar_tempo_hhmmss
        )

        # Gráfico: Duração Média por Centro (Horizontal)
        fig_centro_med = px.bar(
            df_centro_med,
            x="Duração Média",
            y="Centro de Tratamento",
            orientation="h",
            text="Texto_Formatado",
            color="Centro de Tratamento",
            color_discrete_map=MAPA_CORES_CENTROS,
            title="Duração Média de Falhas por Centro",
            template="plotly_white",
        )

        fig_centro_med.update_layout(
            showlegend=False,
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="Duração Média (segundos)",
        )

        # Gráfico: Duração Média por Maquina
        fig_maquina_med = px.bar(
            df_maquina_med,
            x="Nº Máquina",
            y="Duração Média",
            text="Texto_Formatado",
            color="Centro de Tratamento",
            color_discrete_map=MAPA_CORES_CENTROS,
            title="Duração Média de Falhas por Máquina",
            template="plotly_white",
        )

        fig_maquina_med.update_layout(
            yaxis_title="Duração Média (segundos)",
        )

        # Tabela Aba 2 (Duração Média por Máquina)
        df_tabela_med = df_maquina_med.copy()
        df_tabela_med["Centro de Tratamento"] = df_tabela_med[
            "Centro de Tratamento"
        ].str.replace("<br>", " ")
        df_tabela_med["Duração Média"] = df_tabela_med["Texto_Formatado"]
        df_tabela_med = df_tabela_med[
            ["Centro de Tratamento", "Nº Máquina", "Duração Média"]
        ]

        dados_tabela_aba2 = df_tabela_med.to_dict("records")
        colunas_tabela_aba2 = [{"name": i, "id": i} for i in df_tabela_med.columns]

        return (
            kpi_total,
            kpi_media,
            kpi_tempo_total,
            kpi_duracao_media,
            fig_centro_qtd,
            fig_maquina_qtd,
            dados_tabela_aba1,
            colunas_tabela_aba1,
            fig_centro_med,
            fig_maquina_med,
            dados_tabela_aba2,
            colunas_tabela_aba2,
        )

    def registrar_callbacks(self):
        @callback(
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
            [
                # Inputs das datas
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def update_dashboard(start_date_str, end_date_str):
            return self.processar_atualizacao_do_dashboard(start_date_str, end_date_str)
