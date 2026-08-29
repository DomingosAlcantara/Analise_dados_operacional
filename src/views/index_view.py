from datetime import date, timedelta

from dash import dcc, html, page_container

from src.components.back_button import BackButton


class IndexApp:
    """
    Classe principal responsável pelo layout shell (index) e callbacks
    globais.
    """

    ID_URL_LOCATION = "url-location"
    ID_SIDEBAR_CONTAINER = "sidebar-container"
    ID_PAGE_CONTENT = "page-content"
    ID_GLOBAL_DATE_PICKER = "global-date-picker"

    def __init__(self, app_instance) -> None:
        self.app = app_instance
        self.back_button = BackButton()

        # O self.app.layout deve ser definido  pelo método layout
        self.app.layout = self.layout()

    # 1. Método para construir o layout principal (shell)
    def layout(self):
        # Datas padrão para o DatePickerRange global
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        return html.Div(
            [
                # ID para rastrear a URL atual (necessário para multi-páginas e
                # callbacks)
                dcc.Location(id=self.ID_URL_LOCATION, refresh=False),
                # Container que receberá o layout da sidebar
                # (preenchido via callback)
                html.Div(id=self.ID_SIDEBAR_CONTAINER),
                # O conteúdo da página atual (preenchido automaticamente pelo
                # Dash)
                html.Div(
                    [
                        # Cabeçalho com Filtro de Data Global
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H2(
                                            "Período de Análise:",
                                            style={"margin-right": "20px"},
                                        ),
                                        dcc.DatePickerRange(
                                            id=self.ID_GLOBAL_DATE_PICKER,
                                            start_date=str(start_date),
                                            end_date=str(end_date),
                                            display_format="DD/MM/YYYY",
                                            persistence=True,
                                            persistence_type="session",
                                        ),
                                    ],
                                    className="header-date",
                                ),
                                self.back_button.layout(),
                            ],
                            id="header-controls",
                        ),
                        page_container,
                    ],
                    style={"margin-left": "200px", "padding": "25px"},
                ),
            ]
        )
