"""Classe que executará todo o controle (callbacks) sobre a classe 'views.detalhamento'"""

from dash import Input, Output, State, callback, html

from src.controllers.detalhamentos.carga_induzida import CargaInduzidaController
from src.engine import empresa
from src.views.detalhamentos.carga_induzida import CargaInduzida


class Detalhamento:

    def __init__(self):
        """O controller conecta a View aos dados (Model)"""
        self._empresa_model = empresa
        self._carga_induzida_ctrl = CargaInduzidaController()

    def registrar_callbacks(self):
        """Registra os callbacks da página de detalhamento"""

        self._carga_induzida_ctrl.registrar_callbacks()

        @callback(
            Output("colapse-filtros", "is_open"),
            [Input("botao-toggle-filtros", "n_clicks")],
            [State("colapse-filtros", "is_open")],
            prevent_initial_call=True,
        )
        def toggle_collapse(n_clicks, is_open):
            """Alterna a visibilidade do colapso de filtros

            Args:
                n_clicks (int): Número de cliques no botão de toggle.
                is_open (bool): Estado atual do colapso.

            Returns:
                bool: Novo estado do colapso.
            """
            if n_clicks:
                return not is_open
            return is_open

        @callback(
            [
                Output("container-metricas-centro", "style"),
                Output("container-selecao-maquina", "style"),
                Output("container-metricas-maquinas", "style"),
            ],
            Input("detalhamento-nivel-1", "value"),
        )
        def _alternar_visoes(nivel1):
            """Alterna entre as visões do Nível 2 com base na seleção do Nível 1

            Args:
                nivel1 (str): Valor selecionado no Nível 1.

            Returns:
                list: Conteúdo do Nível 2.
            """
            visivel = {"display": "flex"}
            oculto = {"display": "none"}

            if nivel1 == "centro":
                # Mostra o nível 2 do Centro; Esconde os controles de Máquinas
                return visivel, oculto, oculto
            else:
                # Esconde o nível 2 do Centro; Mostra os controles de Máquinas
                return oculto, visivel, visivel

        # Callback para atualizar o gráfico principal
        @callback(
            Output("area-conteudo-principal", "children"),
            [
                Input("detalhamento-nivel-1", "value"),
                Input("detalhamento-metricas-centro", "value"),
                Input("detalhamento-selecao-maquina", "value"),
                Input("detalhamento-metricas-maquinas", "value"),
            ],
        )
        def _atualizar_graficos(
            nivel1, metrica_centro, maquina_selecionada, metrica_maquina
        ):
            """Atualiza os gráficos com base nas seleções dos Níveis 1, 2 e 3

            Args:
                nivel1 (str): Valor selecionado no Nível 1.
                container_nivel_2 (list): Conteúdo do Nível 2.
                container_nivel_3 (list): Conteúdo do Nível 3.

            Returns:
                plotly.graph_objs._figure.Figure: Gráfico atualizado.
            """
            # Lógica para atualizar o gráfico com base nas seleções
            # Aqui você pode acessar os valores selecionados nos níveis 2 e 3
            # e gerar o gráfico correspondente usando Plotly ou outra biblioteca.

            # Descobrir qual metrica atual deve ser usada
            metrica_atual = metrica_centro if nivel1 == "centro" else metrica_maquina

            # 2º passo: Injetar a tela
            if metrica_atual == "carga":
                return CargaInduzida().obter_layout(nivel=nivel1)

            elif metrica_atual == "atolamentos":
                return html.Div(
                    "Tela de Atolamentos em construção...",
                    className="text-center p-5 text-muted fw-bold",
                )

            elif metrica_atual == "falhas_tecnicas":
                return html.Div(
                    "Tela de Falhas Técnicas em construção...",
                    className="text-center p-5 text-muted fw-bold",
                )

            elif metrica_atual == "rejeitos":
                return html.Div(
                    "Tela de Rejeitos em construção...",
                    className="text-center p-5 text-muted fw-bold",
                )

            # Prevenção de erros caso o estado fique vazio
            return html.Div()
