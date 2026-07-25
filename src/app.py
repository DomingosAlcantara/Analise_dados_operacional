import dash
import dash_bootstrap_components as dbc

from src.engine import empresa  # noqa: F401

# Dash
# 1. Instância principal do Dash app
# use_pages = True - habilita o roteamento automático do Dash
# suppress_callback_exceptions = True - Essencial para layouts dinâmicos e
# multi-páginas

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    use_pages=True,
    pages_folder="./views",
    suppress_callback_exceptions=True,
    title="Monitoramento de Máquinas de Triagem de Cartas - CTCE",
)

# Servidor Flask
server = app.server
