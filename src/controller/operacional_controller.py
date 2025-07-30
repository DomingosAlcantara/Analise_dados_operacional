from src.model.operacional_model import OperacionalModel
from src.view.operacional_view import OperacionalView


class OperacionalController:
    """Classe para interligar o modelo e a visualização dos dados operacionais.
    """

    def __init__(self, path) -> None:
        """Inicializa a classe com o modelo e a visualização."""
        self._model = OperacionalModel(path)
        self._view = OperacionalView()

    def mostrar_centros(self):
        """Exibe os centros de tratamento na interface do Streamlit."""
        centros = self._model.get_centro_de_tratamento()
        self._view.exibir_centros(centros)

    def mostrar_maquinas(self):
        """Exibe as máquinas de triagem na interface do Streamlit."""
        maquinas = self._model.get_maquinas()
        self._view.exibir_maquinas(maquinas)
