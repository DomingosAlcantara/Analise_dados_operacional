import pandas as pd
from dash import Input, Output, callback

from src.engine import empresa
from src.views.resumos.falhas_tecnicas import FalhasTecnicas as FalhasTecnicasView


class FalhasTecnicasController:

    def __init__(self):
        self._empresa = empresa
        self._view = FalhasTecnicasView()

    def registrar_callbacks(self):
        @callback(
            [
                # Outputs dos KPIs (Fixos na esquerda)
                Output(self._view.ID_TOTAL_FALHAS, "children"),
                Output(self._view.ID_MEDIA_OBJETOS, "children"),
                Output(self._view.ID_TEMPO_TOTAL, "children"),
                Output(self._view.ID_DURACAO_MEDIA, "figure"),
                # Outputs da aba 1: Quantidades
                Output(self._view.ID_GRAFICO_CENTRO_QTD, "figure"),
                Output(self._view.ID_GRAFICO_MAQUINA_QTD, "figure"),
                Output(self._view.ID_TABELA_MAQUINA_QTD, "children"),
                # Outputs da aba 2: Médias
                Output(self._view.ID_GRAFICO_CENTRO_MED, "figure"),
                Output(self._view.ID_GRAFICO_MAQUINA_MED, "figure"),
                Output(self._view.ID_TABELA_MAQUINA_MED, "children"),
            ],
            [
                # Inputs das datas
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def update_dashboard(start_date_str, end_date_str):
            df_qtd = pd.DataFrame(
                {
                    "Centro de Tratamento": [
                        "CTCE A",
                        "CTCE B",
                    ],
                    "Tempo Total": [
                        "00:03:29",
                        "01:16:11",
                    ],
                    "Tempo Médio": [
                        "00:00:12",
                        "00:00:08",
                    ],
                }
            )

            df_med = pd.DataFrame(
                {
                    "Máquina": [
                        "IND-PBVS1",
                        "IND-PBVS2",
                        "",
                        "IND-PBVS3",
                        "IND-PBVS4",
                        "IND-PBVS5",
                    ],
                    "Tempo Total": [
                        "00:33:01",
                        "00:15:00",
                        "00:10:07",
                        "00:11:03",
                        "00:07:03",
                    ],
                    "Tempo Médio": [
                        "00:00:32",
                        "00:00:12",
                        "00:00:09",
                        "00:00:06",
                        "00:00:05",
                    ],
                }
            )

            kpi_total = "1.245"
            kpi_media = "1.468"
            kpi_tempo_total = "01:35:40"
            kpi_duracao_media = "00:00:11"

            return (
                kpi_total,
                kpi_media,
                kpi_tempo_total,
                kpi_duracao_media,
                self._view.grafico_duracao_media(df=df_qtd),
            )
