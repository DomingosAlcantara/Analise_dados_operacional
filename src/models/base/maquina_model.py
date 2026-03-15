"""Classe para modelagem da máquina de triagem automatizada presente nos
Centros de Tratamento
"""

from pandas import DataFrame


class MaquinaModel:
    """
    Classe base para modelagem de máquinas de triagem automatizadas.
    Esta classe pode ser estendida para incluir atributos e métodos específicos
    relacionados às máquinas de triagem nos centros de tratamento.
    """

    def __init__(self, id_maquina, df: DataFrame):
        self._id_maquina = id_maquina

        if not isinstance(df, DataFrame):
            raise ValueError("O parâmetro 'df' deve ser um DataFrame do pandas.")
        self._df = df[df["nº_máquina"] == self._id_maquina]

    def total_carga_induzida(self) -> int:
        """
        Retorna o total de carga processada pela máquina.

        Returns:
            int: Total de carga processada.
        """
        return int(self._df["quantidade_induzida"].sum())

    def media_carga_induzida(self) -> float:
        """
        Retorna a média de carga processada pela máquina.

        Returns:
            float: Média de carga processada.
        """
        return float(self._df["quantidade_induzida"].mean())

    def media_rendimento_efetivo(self) -> float:
        """
        Retorna o rendimento efetivo da máquina conforme o período, e os planos
        trabalhados.

        Returns:
            float: Rendimento efetivo em porcentagem.
        """
        return float(self._df["rendimento_efetivo/h"].mean())

    def tempo_plano_carregado(self) -> float:
        """
        Retorna o tempo total do plano carregado em horas.

        Returns:
            float: Tempo total do plano em horas.
        """

        def converter_para_horas(tempo_str):
            horas, minutos = map(int, tempo_str.split(":"))
            return horas + minutos / 60.0

        total_tempo = self._df["tempo_total_do_plano"].apply(converter_para_horas).sum()
        return total_tempo

    def listagem_planos_carregados(self) -> list:
        """
        Retorna uma lista dos planos que foram carregados na máquina.

        Returns:
            list: Lista de nomes dos planos carregados.
        """
        return self._df["nome_do_plano_de_triagem"].tolist()
