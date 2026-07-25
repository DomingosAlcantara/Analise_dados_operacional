import dash
from dash import html

from src.components.resumo_card import ResumoCard

# from src.models.carga_induzida_model import CargaInduzidaModel
# from src.utils.cache import cache

try:
    dash.register_page(__name__, path="/", name="Resumos")
except Exception:  # Registro já feito em testes
    pass


class ResumosView:
    """
    Classe para a view de resumos.
    """

    def __init__(self, register_callbacks=True):
        # self.app = app_instance
        self.resumo_card = ResumoCard()

        # correios = cache.get("correios_model")
        # correios._carregar_carga_induzida(
        #     CargaInduzidaModel(PathFiles.ARQUIVOS_CARGA_TRATADA)
        # )

        if register_callbacks:
            self.register_callbacks()

    def register_callbacks(self):
        """
        Registra os callbacks da view de resumos.
        """

    def layout(self):
        """
        Retorna o layout da view de resumos.
        Retorna:
            dash.html.Div: Componente Div contendo o layout da view de resumos.
        """
        return html.Div(
            [
                html.H1(
                    "Resumos",
                    className="resumos-title",
                ),
                self.resumo_card.layout(),
            ],
            className="resumos-view",
        )


def get_layout():
    """
    Retorna o layout da view de resumos.
    Retorna:
        dash.html.Div: Componente Div contendo o layout da view de resumos.
    """

    return ResumosView(register_callbacks=False).layout()


layout = get_layout
