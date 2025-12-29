from dash import html


class KpiCard:
    """
    Classe para criação de cards de indicadores (KPIs)
    """

    def __init__(self, label: str, value: str, card_id=None, extra_class=""):
        """
        Inicializa o card de KPI.

        Args:
            label (str): O rótulo do KPI.
            value (str): O valor do KPI.
            card_id (str, optional): O ID do card. Padrão é None.
            extra_class (str, optional): Classes CSS adicionais para o card.
            Padrão é "".
        """
        self.label = label
        self.value = value
        self.card_id = card_id
        self.extra_class = extra_class

    def display(self):
        """
        Retorna a estrutura HTML do card.

        Returns:
            dash.html.Div: Componente Div contendo o layout do card de KPI.
        """
        # Combinamos a classe base com quaisquer classes extras fornecidas
        full_class_name = f"kpi-block {self.extra_class}".strip()

        h3_props = {"className": "kpi-value"}

        if self.card_id:
            h3_props["id"] = self.card_id

        return html.Div(
            [
                html.P(self.label, className="kpi-label"),
                html.H3(
                    self.value,
                    **h3_props,
                ),
            ],
            className=full_class_name,
        )
