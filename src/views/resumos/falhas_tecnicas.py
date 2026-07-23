from datetime import date, timedelta

import dash
from dash import Input, Output, html

from src.components.kpi_card import KpiCard
from src.components.kpi_graph_card import KpiGraphCard
from src.engine import empresa
from src.models.resumo_model import ResumoModel

try:
    dash.register_page(
        __name__, path="/resumos/falhas-tecnicas", name="Falhas Técnicas"
    )
except Exception:
    # Em ambientes de teste o app pode não estar instanciado ainda. Ignoramos
    # o erro para permitir a importação do módulo sem uma instância do app.
    pass


class FalhasTecnicasView:
    """
    View para exibir o resumo de falhas técnicas,
    """

    def __init__(self, app_instance, register_callbacks=True) -> None:
        self.app = app_instance
        """ Na declaração abaixo devo instanciar a classe resposável pela 
            construção do resumo de falhas técnicas.
        """
        self._resumo_model = ResumoModel(empresa)
        self._TOTAL_FALHAS = "resumo-total-falhas"
        self._MEDIA_OBJETOS_POR_FALHAS = "resumo-media-objetos-por-falhas"
        self._TEMPO_TOTAL_OCORRENCIAS = "resumo-tempo-total-ocorrencias"
        self._DURACAO_MEDIA_FALHAS = "resumo-duracao-media-falhas"

        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=30)

            self._metricas_iniciais = (
                self._resumo_model.retornar_metricas_falhas_tecnicas(
                    start_date, end_date
                )
            )
        except Exception as e:
            print(f"Erro ao calcular métricas iniciais: {e}")
            self._metricas_iniciais = {
                "total_de_falhas": "---",
                "media_objetos_falha": "---",
                "tempo_total_ocorrencias": "---",
                "duracao_media_falha": "---",
            }

        if register_callbacks:
            self.register_callbacks()

    def layout(self) -> html.Div:
        """
        Retorna o layout da página de falhas técnicas.

        Returns:
            html.Div: Componente Div contendo o layout da página.
        """

        card_total_falhas = KpiCard(
            "Total de Falhas",
            str(
                self._metricas_iniciais.get("total_de_falhas", 1)
            ),  # Valor inicial placeholder
            card_id=self._TOTAL_FALHAS,
        )

        card_media_objetos_falhas = KpiCard(
            "Média de Objetos por Falhas",
            str(
                self._metricas_iniciais.get("media_objetos_por_falha", 0)
            ),  # Valor inicial placeholder
            card_id=self._MEDIA_OBJETOS_POR_FALHAS,
        )

        card_tempo_total_ocorrencias = KpiCard(
            "Tempo Total de Ocorrências",
            str(
                self._metricas_iniciais.get("tempo_total_ocorrencias", 0)
            ),  # Valor inicial placeholder
            card_id=self._TEMPO_TOTAL_OCORRENCIAS,
        )

        card_duracao_media_falhas = KpiCard(
            "Duração Média das Falhas",
            str(
                self._metricas_iniciais.get("duracao_media_falha", 0)
            ),  # Valor inicial placeholder
            card_id=self._DURACAO_MEDIA_FALHAS,
        )

        card_qtd_falhas_por_centro = KpiGraphCard(
            figure={},
            graph_id="grafico-falhas-por-centro",
        )

        card_qtd_falhas_por_maquina = KpiGraphCard(
            figure={},
            graph_id="grafico-falhas-por-maquina",
        )

        return html.Div(
            [
                html.Div(  # kpi's de resumo de falhas técnicas, incluindo os cards principais
                    [
                        card_total_falhas.display(),
                        card_media_objetos_falhas.display(),
                        card_tempo_total_ocorrencias.display(),
                        card_duracao_media_falhas.display(),
                    ],
                    style={
                        "width": "100%",
                        "flex": "1",
                    },
                    className="kpi-cards-container",
                ),
                html.Div(  # kpi's dos gráficos de falhas técnicas
                    [
                        html.Div(
                            [
                                html.Div(
                                    card_qtd_falhas_por_centro.display(),
                                    style={
                                        "width": "100%",
                                        "height": "400px",
                                        "flex": "3.5",
                                    },
                                ),
                                html.Div(  # Este gráfico será substituido por uma tabela
                                    card_qtd_falhas_por_maquina.display(),
                                    style={
                                        "width": "100%",
                                        "height": "400px",
                                        "flex": "1.5",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "width": "100%",
                                "height": "400px",
                                "flex": "5",
                            },
                        ),
                        html.Div(
                            card_qtd_falhas_por_maquina.display(),
                            style={
                                "width": "100%",
                                "height": "395px",
                                # "marginTop": "20px",
                            },
                        ),
                    ],
                ),
            ],
            className="kpi-table",
        )

    def register_callbacks(self):
        """
        Registra os callbacks necessários para a página.

        Args:
            app (dash.Dash): Instância do aplicativo Dash.
        """

        @self.app.callback(
            [
                Output(self._TOTAL_FALHAS, "children"),
                Output(self._MEDIA_OBJETOS_POR_FALHAS, "children"),
                Output(self._TEMPO_TOTAL_OCORRENCIAS, "children"),
                Output(self._DURACAO_MEDIA_FALHAS, "children"),
                Output("grafico-falhas-por-centro", "figure"),
                Output("grafico-falhas-por-maquina", "figure"),
            ],
            [
                Input("global-date-picker", "start_date"),
                Input("global-date-picker", "end_date"),
            ],
        )
        def update_falhas_tecnicas(start_date_str, end_date_str):
            # Lógica para atualizar o conteúdo com base no valor de entrada
            return self.falhas_kpis_e_graficos(start_date_str, end_date_str)

    def falhas_kpis_e_graficos(self, start_date_str, end_date_str):
        # Lógica para calcular os KPIs e gerar os gráficos com base no
        # intervalo de datas
        # Aqui você pode acessar os dados, aplicar filtros e retornar os
        # valores atualizados

        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        metricas = self._resumo_model.retornar_metricas_falhas_tecnicas(
            start_date, end_date
        )
        return (
            str(
                metricas.get("total_de_falhas", 0)
            ),  # Exemplo de valor atualizado para o total de falhas
            str(
                metricas.get("media_objetos_por_falha", 0)
            ),  # Exemplo de valor atualizado para a média de objetos por falhas
            "----",  # Exemplo de valor atualizado para o tempo total de ocorrências
            "----",  # Exemplo de valor atualizado para a duração média das falhas
            {},  # Exemplo de figura atualizada para o gráfico de falhas por centro
            {},  # Exemplo de figura atualizada para o gráfico de falhas por máquina
        )


def get_layout() -> html.Div:
    """
    Retorna o layout completo da página, incluindo callbacks.

    Returns:
        html.Div: Componente Div contendo o layout da página.
    """
    from src.app import app

    return FalhasTecnicasView(app, register_callbacks=False).layout()


layout = get_layout
