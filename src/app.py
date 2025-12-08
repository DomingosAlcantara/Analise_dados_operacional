import dash

# 1. Instância principal do Dash app
# use_pages = True - habilita o roteamento automático do Dash
# suppress_callback_exceptions = True - Essencial para layouts dinâmicos e
# multi-páginas

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Monitoramento de Máquinas de Triagem de Cartas - CTCE",
)

# Servidor Flask
server = app.server
