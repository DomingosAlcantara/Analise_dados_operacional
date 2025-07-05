"""
    Esta classe encapsula a lógica de processamento dos dados de resumo,
    incluindo a soma de cargas tratadas e falhas técnicas.
"""


class ResumoModel:
    """
    Classe para gerenciar o resumo de dados.
    """

    def __init__(self, dados):
        self.dados = dados

    def get_dados_resumo(self):
        """
        Método para obter os dados do resumo.
        """
        return self.dados
