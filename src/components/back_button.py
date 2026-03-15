from dash import dcc, html


class BackButton:
    """
    Componente BackButton que representa um botão de voltar.
    """

    def __init__(self) -> None:
        """
        Inicializa o BackButton com o link de destino.

        Args:
            href (str): O link para o qual o botão deve redirecionar.
        """
        self.button_id = "back-button"
        self.container_id = "back-button-container"

    def layout(self) -> html.Div:
        """
        Retorna o layout do botão de voltar.

        Returns:
            dash.html.Div: Componente Div representando o botão de voltar.
        """
        return html.Div(
            dcc.Link(
                html.Button(
                    "← Voltar",
                    id=self.button_id,
                    className="back-button",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            id=self.container_id,
            style={"display": "none"},
        )
