"""Classe para modelagem da carga induzida nas máquinas de triagem
automatizadas nos Centros de Tratamento.
"""


class CargaInduzidaModel:
    """
    Classe base para modelagem da carga induzida.
    Esta classe pode ser estendida para incluir atributos e métodos específicos
    relacionados à carga induzida nas máquinas de triagem nos centros de
    tratamento.
    """

    def __init__(self, quantidade_induzida, status):
        self.quantidade_induzida = quantidade_induzida
        self.status = status
