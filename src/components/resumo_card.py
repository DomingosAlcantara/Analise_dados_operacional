from typing import Dict, List

from dash import dcc, html


class ResumoCard:
    """
    Componente ResumoCard que representa um card de resumo com título e
    conteúdo.
    """

    def __init__(self):
        """
        Classe oara cruar cards de resumo.
        Encapsula a lógica de construção de cards clicáveis.
        """

        self.opcoes: List[Dict[str, str]] = [
            {"titulo": "Carga Induzida", "href": "/resumos/carga-induzida"},
            {"titulo": "Falhas Técnicas", "href": "/resumos/falhas-tecnicas"},
            {"titulo": "Atolamentos", "href": "/resumos/atolamentos"},
        ]

    def set_opcoes(self, opcoes: List[Dict[str, str]]) -> None:
        """
        Define as opções de cards.

        Args:
            opções (List[Dict[str, str]]): Lista com dicionário contendo o
            'título' e 'href' para cada card.
        """
        self.opcoes = opcoes

    def _criar_card(self, opcao: Dict[str, str]) -> html.Div:
        """
        Define as opções de cards.

        Args:
            opcao (Dict[str, str]): Dicionário contendo o 'título' e 'href'.
        Returns:
            html.Div: Componente Div representando o card clicável.
        """
        return html.Div(
            dcc.Link(
                html.Div(
                    [
                        html.H3(opcao["titulo"]),
                    ]
                ),
                href=opcao["href"],
            ),
            className="resumos-card",
        )

    def gerar_cards(self) -> List[html.Div]:
        """
        Gera os cards de resumo com base nas opções definidas.

        Returns:
            List[html.Div]: Lista de Componente Div representando os cards de
            resumo.
        """
        return [self._criar_card(opcao) for opcao in self.opcoes]

    def layout(self) -> html.Div:
        """
        Retorna o layout contendo os cards de resumo.

        Returns:
            html.Div: Componente Div contendo os cards de resumo.
        """
        cards = self.gerar_cards()
        return html.Div(
            cards,
            className="resumos-container",
        )
