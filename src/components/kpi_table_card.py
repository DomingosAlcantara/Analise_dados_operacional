import pandas as pd
from dash import dash_table, html


class KPITableCard:
    """Componente para exibir tabelas de dados padronizados"""

    def __init__(
        self, table_id: str, dados=None, extra_class="", colunas_esquerda=None
    ):
        self.table_id = table_id
        self.dados = dados
        self.extra_class = extra_class
        # Agora recebemos apenas uma lista com os nomes das colunas! Ex: ["Centro de Tratamento"]
        self.colunas_esquerda = colunas_esquerda or []

    def display(self):
        full_class_name = f"kpi-table-container {self.extra_class}".strip()

        if (
            self.dados is None
            or (isinstance(self.dados, pd.DataFrame) and self.dados.empty)
            or self.dados == []
        ):
            colunas = [{"name": "Aguardando dados...", "id": "placeholder"}]
            conteudo = [{"placeholder": "Sem informações no período"}]
        elif isinstance(self.dados, pd.DataFrame):
            colunas = [{"name": col, "id": col} for col in self.dados.columns]
            conteudo = self.dados.to_dict("records")
        else:
            colunas = [{"name": k, "id": k} for k in self.dados[0].keys()]
            conteudo = self.dados

        # -------------------------------------------------------------
        # MÁGICA AQUI: O componente constrói a regra do Dash sozinho
        # -------------------------------------------------------------
        regras_alinhamento = []
        for col in self.colunas_esquerda:
            regras_alinhamento.append({"if": {"column_id": col}, "textAlign": "left"})

        return html.Div(
            [
                dash_table.DataTable(
                    id=self.table_id,
                    columns=colunas,
                    data=conteudo,
                    page_action="none",
                    style_table={"overflowY": "auto"},
                    # 1. Títulos SEMPRE centralizados
                    style_header={
                        "textAlign": "center",
                        "fontWeight": "bold",
                        "backgroundColor": "#f8f9fa",
                    },
                    # 2. Todas as células centralizadas por padrão
                    style_cell={
                        "textAlign": "center",
                        "padding": "8px",
                        "fontFamily": "sans-serif",
                    },
                    # 3. Regra de exceção aplicada apenas nas colunas que passamos na lista
                    style_cell_conditional=regras_alinhamento,
                )
            ],
            className=full_class_name,
        )
