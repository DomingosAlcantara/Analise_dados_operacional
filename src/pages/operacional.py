from src.controller.operacional_controller import OperacionalController


class Operacional:

    def __init__(self) -> None:
        self._path = "C:/Users/80891950/Downloads/Relatório Pitney Bower/Dados/Operacional/"
        self.controller = OperacionalController(self._path)

    def mostrar_centros(self):
        """Função para exibir os centros de tratamento."""
        self.controller.mostrar_centros()

    def mostrar_maquinas(self):
        """Função para exibir as máquinas de triagem."""
        self.controller.mostrar_maquinas()


operacional = Operacional()
operacional.mostrar_centros()
operacional.mostrar_maquinas()
