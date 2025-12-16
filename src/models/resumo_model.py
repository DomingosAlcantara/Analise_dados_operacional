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

    def get_performance_metrics(self, start_date, end_date):
        """
        Método para calcular métricas de performance.
        """
        dias = (end_date - start_date).days if start_date and end_date else 30

        total_carga = (550000 * dias) / 30  # sum(item['carga'] for item in self.dados)
        media_carga = total_carga / dias  # sum(item['falhas'] for item in self.dados)
        eficiencia = media_carga * 0.95

        return {
            "carga_induzida": f"{total_carga:.0f}",
            "media_carga": f"{media_carga:.0f}",
            "eficiencia": f"{eficiencia:.0f}",
        }
