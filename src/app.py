from dash import Dash, dcc, html

app = Dash()

app.layout = html.Div(
    [
        html.Div(
            [
                html.H3("Opções de Navegação"),
                html.P("Filtros e Controles aqui..."),
                dcc.Dropdown(
                    options=[
                        {"label": "Opção 1", "value": "1"},
                        {"label": "Opção 2", "value": "2"},
                        {"label": "Opção 3", "value": "3"},
                    ],
                    value="1",
                ),
            ],
            style={
                "width": "20%",
                "display": "inline-block",
                "verticalAlign": "top",
                "padding": "10px",
                "borderRight": "1px solid #ccc",
            },
        ),
        html.Div(
            [
                html.H1("Conteúdo Principal"),
            ],
            style={
                "width": "80%",
                "display": "inline-block",
                "padding": "10px",
                "marginLeft": "5%",
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
