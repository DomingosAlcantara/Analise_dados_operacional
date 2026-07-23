"""
Esta classe encapsula a lógica de processamento dos dados de resumo,
incluindo a soma de cargas tratadas e falhas técnicas.
"""

import math


def _pt_format_number(n: float, decimals: int) -> str:
    """
    Formata um número para o padrão brasileiro com separador de milhar
    como ponto e decimal como vírgula.

    Args:
        n (float): Número a ser formatado.
        decimals (int): Número de casas decimais.

    Returns:
        str: Número formatado no padrão brasileiro.
    """
    s = f"{n:,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


class ResumoModel:
    """
    Classe para gerenciar o resumo de dados.
    """

    def __init__(self, empresa):
        """
        Inicializa o modelo de resumo.
        """
        self._empresa = empresa

    def formatacao_compacta_de_valores(self, v):
        try:
            if v is None or (isinstance(v, float) and math.isnan(v)):
                return "—"
            val = float(v)
            if abs(val) >= 1_000_000:
                return f"{_pt_format_number(val / 1_000_000, 2)} M"
            if abs(val) >= 1_000:
                return f"{_pt_format_number(val / 1_000, 1)} Mil"
            return _pt_format_number(val, 0)
        except Exception:
            return "—"

    def get_performance_metrics(self, start_date, end_date):
        """
        Método para calcular métricas de performance.
        """
        self._empresa.definir_intervalo_de_pesquisa(start_date, end_date)
        print(f"Calculando métricas para o período de {start_date} a {end_date}...")

        return {
            "carga_induzida": self.formatacao_compacta_de_valores(
                self._empresa.retornar_carga_induzida_total()
            ),
            "media_carga": self.formatacao_compacta_de_valores(
                self._empresa.retornar_media_diaria()
            ),
            "eficiencia": self.formatacao_compacta_de_valores(
                self._empresa.retornar_rendimento_efetivo_medio()
            ),
        }

    def carga_induzida_por_centro(self):
        """
        Método para obter a carga induzida por centro.
        """
        return self._empresa.retornar_carga_induzida_por_centro()

    def rendimento_efetivo_por_centro(self):
        """
        Método para obter o rendimento efetivo por centro.
        """
        return self._empresa.retornar_rendimento_efetivo_por_centro()

    def carga_induzida_por_maquina(self):
        """
        Método para obter a carga induzida por máquina.
        """
        return self._empresa.retornar_carga_induzida_por_maquina()

    def rendimento_efetivo_por_maquina(self):
        """
        Método para obter o rendimento efetivo por máquina.
        """
        return self._empresa.retornar_rendimento_efetivo_por_maquina()

    def _adicionar_rotulo_maquina(self, df):
        """
        Adiciona uma coluna 'Rótulo Máquina' ao DataFrame com o formato
        'Máquina {Nº Máquina} - Centro {Centro de Tratamento}'.

        Args:
            df (pandas.DataFrame): DataFrame contendo as colunas
            'Nº Máquina' e 'Centro de Tratamento'.

        Returns:
            pandas.DataFrame: DataFrame com a nova coluna 'Rótulo Máquina'.
        """
        return self._empresa.retornar_carga_induzida_por_maquina()
