""" Classe para modelagem dos turnos de trabalho das máquinas de triagem
    automatizadas nos Centros de Tratamento.
"""


class TurnoModel():
    """
        Classe base para modelagem dos turnos de trabalho.
        Esta classe pode ser estendida para incluir atributos e métodos
        específicos relacionados aos turnos de trabalho das máquinas de triagem
        automatizadas.
    """

    def __init__(self, id_turno, horario, df):
        self.id_turno = id_turno
        self._hora_inicio, self._hora_fim = horario.values()
        self._df = self._extrair_carga_turno(df)

    def _extrair_carga_turno(self, df):
        """
        Extrai os dados de carga do DataFrame para o turno específico.

        Returns:
            DataFrame: Dados filtrados para o turno.
        """
        return df[
            (df["hora_inicial_de_triagem"] >= self._hora_inicio) &
            (df["hora_final_de_triagem"] <= self._hora_fim)
        ]

    def total_carga_induzida_maquina(self) -> int:
        """
        Retorna o total de carga induzida pela máquina durante o turno.

        Returns:
            int: Total de carga induzida.
        """
        return int(self._df[
            (self._df["hora_inicial_de_triagem"] >= self._hora_inicio) &
            (self._df["hora_final_de_triagem"] <= self._hora_fim)
        ]["quantidade_induzida"].sum())

    def rendimento_efetivo_maquina(self) -> float:
        """
        Retorna o rendimento efetivo da máquina durante o turno.

        Returns:
            float: Rendimento efetivo (carga/hora).
        """
        return float(self._df["rendimento_efetivo/h"].sum() / len(self._df))
