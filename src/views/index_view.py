from dash import dcc, html, page_container

from src.components.header_controls import HeaderControls


class IndexApp:
    """
    Classe principal responsável pelo layout shell (index) e callbacks
    globais.
    """

    ID_URL_LOCATION = "url-location"
    ID_SIDEBAR_CONTAINER = "sidebar-container"

    def __init__(self, app_instance) -> None:
        self.app = app_instance
        self.header_controls = HeaderControls()

        # O self.app.layout deve ser definido  pelo método layout
        self.app.layout = self.layout()

    # 1. Método para construir o layout principal (shell)
    def layout(self) -> html.Div:
        return html.Div(
            [
                # ID para rastrear o URL atual
                dcc.Location(id=self.ID_URL_LOCATION, refresh=False),
                # Container que receberá o layout da sidebar
                html.Div(id=self.ID_SIDEBAR_CONTAINER),
                # Container do conteúdo principal
                html.Div(
                    [
                        # Cabeçalho encapsulado
                        self.header_controls.layout(),
                        # O conteúdo da página renderizado pelo Dash Pages
                        page_container,
                    ],
                    className="main-content-container",
                ),
            ]
        )
