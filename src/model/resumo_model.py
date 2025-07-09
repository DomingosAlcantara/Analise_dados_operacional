from uteis import Uteis


class ResumoModel(Uteis):
    """Classe para o modelo de resumo dos dados.
    """

    def __init__(self, data):
        self._data = None
        self._set_dados(data)

    def get_soma_carga_induzida(self, data_pretendida):
        """_summary_

        Args:
            data_pretendida (_type_): _description_
        """
