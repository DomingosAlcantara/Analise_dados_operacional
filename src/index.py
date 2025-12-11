from datetime import date, timedelta

from dash import Input, Output, dcc, html, page_container

from src.app import app

# Importa a instância da classe Sidebar
from src.components.sidebar import sidebar_component as Sidebar


class IndexApp:
    """
    Classe principal responsável pelo layout shell (index) e callbacks
    globais.
    """

    def __init__(self, app_instance) -> None:
        self.app = app_instance
        # Define IDs globais
        self.url_location_id = "url-location"
        self.sidebar_container_id = "sidebar-container"
        self.page_content_id = "page-content"
        self.global_date_picker_id = "global-date-picker"

        # O self.app.layout deve ser definido  pelo método layout
        self.app.layout = self.layout()

        # Chama o método para registrar os callbaks
        self.register_callbacks()

    # 1. Método para construir o layout principal (shell)
    def layout(self):
        # Datas padrão para o DatePickerRange global
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        return html.Div(
            [
                # ID para rastrear a URL atual (necessário para multi-páginas e
                # callbacks)
                dcc.Location(id=self.url_location_id, refresh=False),
                # Container que receberá o layout da sidebar
                # (preenchido via callback)
                html.Div(id=self.sidebar_container_id),
                # O conteúdo da página atual (preenchido automaticamente pelo
                # Dash)
                html.Div(
                    [
                        # Cabeçalho com Filtro de Data Global
                        html.Div(
                            [
                                html.H4(
                                    "Período de Análise:",
                                    style={"margin-right": "20px"},
                                ),
                                dcc.DatePickerRange(
                                    id=self.global_date_picker_id,
                                    start_date=str(start_date),
                                    end_date=str(end_date),
                                    display_format="DD/MM/YYYY",
                                    persistence=True,
                                    persistence_type="session",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "right": "250px",
                                "padding": "15px",
                                "backgroundColor": "#f8f9fa",
                                "borderBottom": "1px solid #dee2e6",
                                "marginBottom": "25px",
                            },
                        ),
                        page_container,
                    ],
                    style={"margin-left": "200px", "padding": "25px"},
                ),
            ]
        )

    # 2. Método para registrar callbacks globais
    def register_callbacks(self):
        """
        Callback para atualizar e renderizar a Sidebar com o estado ativo.
        """

        @self.app.callback(
            Output(self.sidebar_container_id, "children"),
            Input(self.url_location_id, "pathname"),
            allow_duplicate=True,
        )
        def update_sidebar(pathname):
            """Atualiza a Sidebar com o item ativo baseado na URL atual.

            Args:
                pathname (str): Caminho da URL atual.

            Returns:
                Sidebar: Componente Sidebar atualizado.
            """
            return Sidebar.layout(current_path=pathname)


# 3. INSTÂNCIA E EXECUÇÃO

# 3.1. Importar as páginas é CRUCIAL para que o Dash as registre.
# Você precisa garantir que todos os módulos em 'pages/' sejam importados.
# Isso popula o 'dash.page_registry' antes de rodar o servidor.
# O Dash, ao usar use_pages=True, normalmente faz isso automaticamente ao
# escanear a pasta 'pages/', mas uma importação explícita garante que
# os callbacks das classes das páginas também sejam registrados.


# 3.2. Criamos a instância da classe principal
# Isso define app.layout e registra o callback de roteamento da sidebar
# main_app_instance = IndexApp(app)
if __name__ == "__main__":
    index_app = IndexApp(app)

    import views.analise_operacional  # noqa: E402, F401
    import views.comparativo  # noqa: E402, F401
    import views.monitoramento  # noqa: E402, F401
    import views.resumo  # noqa: E402, F401

    app.run(debug=True)
