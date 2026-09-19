from datetime import date, timedelta

from dash import dcc, html

from src.components.back_button import BackButton


class HeaderControls:
    """Componente resposável pela barra superior, contendo o filtro de data
    global e o botão de voltar
    """

    ID_GLOBAL_DATE_PICKER = "global-date-picker"

    def __init__(self):
        self.back_button = BackButton()

    def layout(self) -> html.Div:
        # Datas padrão para o DatePickerRange global
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        return html.Div(
            [
                # Bloco da Esquerda: Titulo e Filtro de Data Global
                html.Div(
                    [
                        html.H2(
                            "Período de Análise:",
                            className="header-title",
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
                # Container protetor para o botão não ser esmagado
                html.Div(self.back_button.layout(), className="back-button-wrapper"),
            ],
            id="header-controls",
            className="header-controls-container",
        )
