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
        self._horarios = self._definir_formato_hora(horarios,
                                                    ["horario_inicio",
                                                     "horario_final"])
        self._dados = self._definir_formato_hora(
            df, ["hora_inicial_de_triagem", "hora_final_de_triagem"]
        )

    def _definir_formato_hora(self, df: DataFrame,
                              colunas: list = None) -> DataFrame:
        """
        Converte colunas de horário para datetime.time usando transformações 
        funcionais.

        Args:
            df (DataFrame): DataFrame com as colunas de horário
            colunas (list, optional): Lista de colunas para converter

        Returns:
            DataFrame: Novo DataFrame com as colunas convertidas
        """
        def converter_para_time(coluna: str) -> pd.Series:
            return pd.to_datetime(df[coluna], format="%H:%M").dt.time

        # Usa colunas padrão se nenhuma for especificada
        colunas_para_converter = colunas or ["horario_inicio", "horario_final"]

        # Filtra apenas colunas que existem no DataFrame
        colunas_validas = filter(
            lambda col: col in df.columns, colunas_para_converter)

        # Cria novo DataFrame com as conversões
        return df.assign(**{
            coluna: converter_para_time(coluna)
            for coluna in colunas_validas
        })

    def total_carga_induzida_maquina(self) -> dict:
        """
        Retorna o total de carga induzida pela máquina durante o turno.

        Returns:
            dict: Total de carga induzida.
        """

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
