""" Classe para modelagem dos turnos de trabalho das máquinas de triagem
    automatizadas nos Centros de Tratamento.
"""


import pandas as pd
from pandas import DataFrame


class TurnoModel():
    """
        Classe base para modelagem dos turnos de trabalho.
        Esta classe pode ser estendida para incluir atributos e métodos
        específicos relacionados aos turnos de trabalho das máquinas de triagem
        automatizadas.
    """

    def __init__(self, horarios, df):
        self._horarios = self._formatar_horario(horarios)
        self._dados = df.copy()

    def _formatar_horario(self, horario: DataFrame):
        """
        Formata uma string de horário no formato "HH:MM" para um objeto
        datetime.time.

        Args:
            horario_str (str): String de horário no formato "HH:MM".

        Returns:
            datetime.time: Objeto de tempo correspondente.
        """
        horario["horario_inicio"] = pd.to_datetime(
            horario["horario_inicio"], format="%H:%M").dt.time

        horario["horario_final"] = pd.to_datetime(
            horario["horario_final"], format="%H:%M").dt.time

        return horario

    def total_carga_induzida_maquina(self) -> dict:
        """
        Retorna o total de carga induzida pela máquina durante o turno.

        Returns:
            dict: Total de carga induzida.
        """

        self._dados["hora_inicial_de_triagem"] = pd.to_datetime(
            self._dados["hora_inicial_de_triagem"], format="%H:%M").dt.time

        self._dados["hora_final_de_triagem"] = pd.to_datetime(
            self._dados["hora_final_de_triagem"], format="%H:%M").dt.time

        resultado = {}

        for _, turno in self._horarios.iterrows():
            inicio = turno["horario_inicio"]
            fim = turno["horario_final"]

            mascara_turno = (
                (self._dados["hora_inicial_de_triagem"] >= inicio) &
                (self._dados["hora_final_de_triagem"] <= fim)
            )

            df_turno = self._dados[mascara_turno]

            cargas = df_turno.groupby("nº_máquina")["quantidade_induzida"].sum()

            resultado[turno["id"]] = cargas.to_dict()

        return resultado

    def rendimento_efetivo_maquina(self) -> float:
        """
        Retorna o rendimento efetivo da máquina durante o turno.

        Returns:
            float: Rendimento efetivo (carga/hora).
        """
        return float(self._dados["rendimento_efetivo/h"].sum() / len(self._dados))
