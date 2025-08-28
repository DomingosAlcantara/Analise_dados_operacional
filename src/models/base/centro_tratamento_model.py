""" Classe para modelagem dos Centros de Tratamento de Cargas e
    Encomendas dos Correios.
"""


class CentroTratamentoModel():
    """
    Classe base para modelagem dos Centros de Tratamento.
    Esta classe pode ser estendida para incluir atributos e métodos específicos
    relacionados aos centros de tratamento de cargas e encomendas.
    """

    def __init__(self, id_centro):
        self.id_centro = id_centro
        self.maquinas = []
