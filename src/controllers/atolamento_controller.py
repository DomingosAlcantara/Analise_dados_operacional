from src.models.atolamentos_model import AtolamentosModel
from src.views.atolamentos import AtolamentosView


class AtolamentoController:
    def __init__(self):
        self.modelo = AtolamentosModel()
        self.view = AtolamentosView(self.modelo)

    def processar_dados(self):
        """
        Processa os dados de atolamentos.
        """
        # Implementação do processamento de dados
        pass

    def get_dados(self):
        """
        Retorna os dados de atolamentos processados.
        """
        if self._dados is None:
            self.processar_dados()
        if self._dados is None:
            raise ValueError("Os dados de atolamentos não foram carregados.")
        return self._dados
