from dash import html


class Grid:
    """
    Fábrica de componentes estruturais padronizados da aplicação.
    Centraliza a criação de linhas, colunas e grids
    """

    @staticmethod
    def coluna(children, style=None, class_name="", id=None):
        """
        Cria uma coluna flexivel (itens espalhados verticalmente).

        Args:
            children (list): Lista de componentes filhos.
            style (dict, optional): Estilos CSS para a coluna.
            class_name (str, optional): Classes CSS adicionais para a coluna.
            id (str, optional): ID para a coluna.

        Returns:
            dash.html.Div: Componente Div representando a coluna.
        """
        default_style = {
            "display": "flex",
            "flexDirection": "column",
            "height": "84vh",  # Ajuste conforme necessário
            "gap": "0px",  # Espaçamento entre os elementos
        }

        if style:
            default_style.update(style)

        kwargs = {}
        if id:
            kwargs["id"] = id
        if class_name:
            kwargs["className"] = class_name

        return html.Div(children, style=default_style, **kwargs)

    @staticmethod
    def linha(children, style=None, class_name="", id=None):
        """
        Cria uma linha (row) com os filhos fornecidos.

        Args:
            children (list): Lista de componentes filhos.
            style (dict, optional): Estilos CSS para a linha.
            class_name (str, optional): Classes CSS adicionais para a linha.
            id (str, optional): ID para a linha.

        Returns:
            dash.html.Div: Componente Div representando a linha.
        """
        default_style = {
            "display": "flex",
            "flexDirection": "row",
            "height": "100%",
            "gap": "0px",
        }

        if style:
            default_style.update(style)

        kwargs = {}
        if id:
            kwargs["id"] = id
        if class_name:
            kwargs["className"] = class_name

        return html.Div(children, style=default_style, **kwargs)
