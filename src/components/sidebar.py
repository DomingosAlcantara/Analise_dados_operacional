from typing import Any

from dash import dcc, html, page_registry


class Sidebar:
    """
    Componente Sidebar que gera a barra lateral de navegação
    e gerencia o estado ativo dos links.
    """

    def __init__(self):
        """Inicializa a classe Sidebar."""
        # Lista dos nomes das páginas na ordem desejada
        self.ordered_page = [
            "Resumos",
            "Detalhamento",
        ]

    def layout(self, current_path: str):
        """Retorna o layout da barra lateral.

        Args:
            current_path (str): O caminho atual da página para determinar o
            link ativo.

        Returns:
            dash.html.Div: Componente Div contendo o layout da barra lateral.
        """
        # Mapeia todos os nomes das páginas registradas pelo Dash
        all_pages: dict[str, Any] = {
            page["name"]: page for page in page_registry.values()
        }

        # Monta a ordem final: primeiro os nomes definidos em `ordered_page`
        # (se existirem), depois as demais páginas registradas (ordenadas por nome).
        ordered_names = [name for name in self.ordered_page if name in all_pages]
        remaining = sorted([n for n in all_pages if n not in ordered_names])

        # Mapeia os nomes visíveis no sidebar para o objeto Page do Dash
        self.page_map: dict[str, Any] = {
            name: all_pages[name] for name in ordered_names + remaining
        }

        nav_links = []

        # Gera os links de navegação com base na ordem definida
        for name in self.ordered_page:
            if name in self.page_map:
                page = self.page_map[name]

                # Verifica se o caminho da página é igual ao caminho atual
                is_active = page["path"] == current_path

                nav_links.append(
                    html.Div(
                        dcc.Link(
                            name,
                            href=page["path"],
                            className=f"nav-link{' active'
                                                 if is_active else ''}",
                        ),
                        className="nav-item_wrapper",
                    )
                )

        return html.Div(
            id="sidebar",
            children=[
                html.H1("Menu de Navegação", className="logo"),
                html.Nav(nav_links),
            ],
        )


# Instância global da Sidebar
# Isso permite reutilizar a mesma instância em diferentes partes da aplicação
sidebar_component = Sidebar()
