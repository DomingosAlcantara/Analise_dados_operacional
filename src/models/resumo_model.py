"""
Esta classe encapsula a lógica de processamento dos dados de resumo,
incluindo a soma de cargas tratadas e falhas técnicas.
"""

import math


class ResumoModel:
    """
    Classe para gerenciar o resumo de dados.
    """

    def __init__(self, model_carga_induzida):
        """
        Inicializa o modelo de resumo.
        """
        self._model_carga_induzida = model_carga_induzida

    # def get_dados_resumo(self):
    #     """
    #     Método para obter os dados do resumo.
    #     """
    #     return self._dados

    def get_performance_metrics(self, start_date, end_date):
        """
        Método para calcular métricas de performance.
        """
        # dias = (end_date - start_date).days if start_date and end_date
        # else 30
        self._model_carga_induzida.filtrar_dados_por_data(start_date, end_date)

        total_carga = self._model_carga_induzida.total_de_carga_induzida()
        media_carga = self._model_carga_induzida.media_carga_induzida()
        eficiencia = self._model_carga_induzida.rendimento_efetivo_hora()

        def fmt(v):
            try:
                if v is None or (isinstance(v, float) and math.isnan(v)):
                    return "—"
                return f"{v:.0f}"
            except Exception:
                return "—"

        return {
            "carga_induzida": fmt(total_carga),
            "media_carga": fmt(media_carga),
            "eficiencia": fmt(eficiencia),
        }

    def carga_induzida_por_centro(self):
        """
        Método para obter a carga induzida por centro.
        """
        return self._model_carga_induzida.carga_induzida_por_centro()

    def rendimento_efetivo_por_centro(self):
        """
        Método para obter o rendimento efetivo por centro.
        """
        return self._model_carga_induzida.rendimento_efetivo_por_centro()

    def carga_induzida_por_maquina(self):
        """
        Método para obter a carga induzida por máquina.
        """
        return self._model_carga_induzida.carga_induzida_por_maquina()

    def rendimento_efetivo_por_maquina(self):
        """
        Método para obter o rendimento efetivo por máquina.
        """
        return self._model_carga_induzida.rendimento_efetivo_por_maquina()
