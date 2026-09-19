from dash import html


class Grid:
    """
    Fábrica de componentes estruturais padronizados da aplicação.
    Centraliza a criação de linhas, colunas e grids
    """

    @staticmethod
    def coluna(children, style=None, class_name="", id=None, tamanho=None, **kwargs):
        """
        Cria uma coluna flexivel (itens espalhados verticalmente).

        Args:
            children (list): Lista de componentes filhos.
            style (dict, optional): Estilos CSS para a coluna.
            class_name (str, optional): Classes CSS adicionais para a coluna.
            id (str, optional): ID para a coluna.
            tamanho (int, optional): Largura da coluna em um grid de 12 (Ex: 6 = 50%, 12 = 100%).

        Returns:
            dash.html.Div: Componente Div representando a coluna.
        """
        merged_style = {}

        if tamanho is not None:
            percentual = (tamanho / 12.0) * 100
            merged_style["width"] = f"{percentual}%"
            merged_style["flex"] = f"0 0 {percentual}%"

        if style:
            merged_style.update(style)

        final_class = f"grid-coluna {class_name}".strip()

        props = {"className": final_class}

        if merged_style:
            props["style"] = merged_style
        if id:
            props["id"] = id

        props.update(kwargs)

        return html.Div(children, **props)

    @staticmethod
    def linha(children, style=None, class_name="", id=None, **kwargs):
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
        merged_style = {}

        if style:
            merged_style.update(style)

        final_class = f"grid-linha {class_name}".strip()

        props = {"className": final_class}

        if merged_style:
            props["style"] = merged_style
        if id:
            props["id"] = id

        props.update(kwargs)

        return html.Div(children, **props)
