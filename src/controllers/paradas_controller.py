from src.models.paradas_model import ParadasModel
from src.views.paradas_view import ParadasView


class ParadasController:
    def __init__(self, files_path="/home/domingos/Documentos/Dados/Engarrafamento/"):
        self.modelo = ParadasModel(files_path)
        self.view = ParadasView()

    def exibir_maquinas(self):
        """
        Exibe as máquinas existentes no Centro de Tratamento.
        """
        maquinas = self.modelo.mostrar_maquinas()
        self.view.mostrar_maquinas(maquinas)

    def exibir_grafico_percentual_paradas(self):
        """
        Exibe os dados de atolamento de cartas do CTCE.
        """
        paradas = self.modelo.get_paradas_em_percentual()
        self.view.mostrar_paradas(
            paradas if paradas is not None else ("Nenhuma parada registrada.", 0)
        )

    def get_maiores_paradas(self, n):
        """
        Obtém os maiores atolamentos.

        :param n: Número de maiores atolamentos a serem retornados.
        :return: DataFrame com os maiores atolamentos.
        """
        maiores_paradas = self.modelo.get_maiores_paradas(n)
        return maiores_paradas if maiores_paradas is not None else 0

    def get_soma_geral_paradas(self):
        """
        Obtém a soma geral dos atolamentos.

        :return: Soma geral dos atolamentos.
        """
        soma_geral = self.modelo.get_soma_geral_paradas()
        return soma_geral if soma_geral is not None else 0
